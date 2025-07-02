#!/bin/bash

set -e

# 변수 설정
REGION="ap-northeast-2"
BUCKET_NAME="firehose-test-bucket-$(date +%s)"
FIREHOSE_STREAM_NAME="test-firehose-stream"
IAM_ROLE_NAME="firehose-delivery-role"

echo "🚀 Firehose 리소스 생성 시작..."
echo "리전: $REGION"
echo "S3 버킷: $BUCKET_NAME"
echo "Firehose 스트림: $FIREHOSE_STREAM_NAME"
echo "=================================="

# 1. S3 버킷 생성
echo "📦 S3 버킷 생성 중..."
aws s3 mb s3://$BUCKET_NAME --region $REGION
echo "✅ S3 버킷 생성 완료: $BUCKET_NAME"

# 2. Firehose 서비스 역할을 위한 신뢰 정책 생성
echo "🔐 IAM 역할 생성 중..."
cat > /tmp/firehose-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# 3. IAM 역할 생성
aws iam create-role \
  --role-name $IAM_ROLE_NAME \
  --assume-role-policy-document file:///tmp/firehose-trust-policy.json \
  --region $REGION || echo "⚠️  역할이 이미 존재하거나 생성 실패"

# 4. S3 접근 권한 정책 생성
cat > /tmp/firehose-s3-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::$BUCKET_NAME",
        "arn:aws:s3:::$BUCKET_NAME/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:$REGION:*:*"
    }
  ]
}
EOF

# 5. 인라인 정책 연결
aws iam put-role-policy \
  --role-name $IAM_ROLE_NAME \
  --policy-name "FirehoseS3DeliveryPolicy" \
  --policy-document file:///tmp/firehose-s3-policy.json

echo "✅ IAM 역할 생성 완료: $IAM_ROLE_NAME"

# 6. 계정 ID 가져오기
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$IAM_ROLE_NAME"

# 7. IAM 역할 전파 대기 (AWS 일관성 지연 해결)
echo "⏳ IAM 역할 전파 대기 중... (30초)"
sleep 30

# 8. 역할 존재 확인
echo "🔍 IAM 역할 존재 확인 중..."
for i in {1..5}; do
  if aws iam get-role --role-name $IAM_ROLE_NAME >/dev/null 2>&1; then
    echo "✅ IAM 역할 확인 완료"
    break
  else
    echo "⏳ 역할 확인 재시도 ($i/5)..."
    sleep 10
  fi
done

echo "🔥 Firehose 스트림 생성 중..."

# 9. Firehose 스트림 생성
aws firehose create-delivery-stream \
  --delivery-stream-name $FIREHOSE_STREAM_NAME \
  --delivery-stream-type DirectPut \
  --s3-destination-configuration \
    RoleARN=$ROLE_ARN,BucketARN=arn:aws:s3:::$BUCKET_NAME,Prefix=firehose-data/,BufferingHints='{SizeInMBs=1,IntervalInSeconds=60}',CompressionFormat=UNCOMPRESSED \
  --region $REGION

echo "✅ Firehose 스트림 생성 완료: $FIREHOSE_STREAM_NAME"

# 10. 생성된 리소스 정보 출력
echo ""
echo "🎉 리소스 생성 완료!"
echo "=================================="
echo "S3 버킷: $BUCKET_NAME"
echo "Firehose 스트림: $FIREHOSE_STREAM_NAME"
echo "IAM 역할: $IAM_ROLE_NAME"
echo "리전: $REGION"
echo ""
echo "📝 Python 스크립트에서 사용할 정보:"
echo "FIREHOSE_STREAM_NAME = '$FIREHOSE_STREAM_NAME'"
echo "REGION = '$REGION'"
echo ""

# 11. 임시 파일 정리
rm -f /tmp/firehose-trust-policy.json /tmp/firehose-s3-policy.json

echo "🧹 임시 파일 정리 완료"
echo "✨ 모든 작업이 완료되었습니다!"

import boto3
import json
import time
import random
import string
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

class FirehoseDataSender:
    def __init__(self, stream_name, region='ap-northeast-2', role_arn=None):
        self.stream_name = stream_name
        self.region = region
        self.role_arn = role_arn
        
        try:
            if role_arn:
                # IAM 역할을 assume하여 자격증명 획득
                print(f"🔐 IAM 역할 사용: {role_arn}")
                sts_client = boto3.client('sts', region_name=region)
                
                assumed_role = sts_client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName='firehose-test-session'
                )
                
                credentials = assumed_role['Credentials']
                
                self.firehose_client = boto3.client(
                    'firehose',
                    region_name=region,
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken']
                )
                print(f"✅ IAM 역할 기반 Firehose 클라이언트 초기화 완료")
            else:
                # 기본 자격증명 사용
                self.firehose_client = boto3.client('firehose', region_name=region)
                print(f"✅ 기본 자격증명으로 Firehose 클라이언트 초기화 완료 (리전: {region})")
                
        except NoCredentialsError:
            print("❌ AWS 자격 증명이 설정되지 않았습니다.")
            exit(1)
        except ClientError as e:
            print(f"❌ IAM 역할 assume 실패: {e}")
            print("💡 기본 자격증명으로 재시도...")
            try:
                self.firehose_client = boto3.client('firehose', region_name=region)
                print(f"✅ 기본 자격증명으로 Firehose 클라이언트 초기화 완료")
            except Exception as fallback_error:
                print(f"❌ 모든 자격증명 방법 실패: {fallback_error}")
                exit(1)
    
    def generate_random_data(self):
        """임의의 테스트 데이터 생성"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": f"user_{random.randint(1000, 9999)}",
            "event_type": random.choice(["login", "logout", "purchase", "view", "click"]),
            "message": ''.join(random.choices(string.ascii_letters + string.digits, k=50)),
            "value": random.randint(1, 1000),
            "session_id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        }
        return json.dumps(data) + '\n'
    
    def send_single_record(self, data=None):
        """단일 레코드 전송"""
        if data is None:
            data = self.generate_random_data()
        
        try:
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={
                    'Data': data.encode('utf-8')
                }
            )
            
            print(f"✅ 단일 레코드 전송 성공")
            print(f"   RecordId: {response['RecordId']}")
            print(f"   데이터 크기: {len(data)} bytes")
            print(f"   전송 데이터: {data.strip()}")
            return True
            
        except ClientError as e:
            print(f"❌ 단일 레코드 전송 실패: {e}")
            return False
    
    def send_batch_records(self, count=5):
        """배치 레코드 전송"""
        records = []
        
        for i in range(count):
            data = self.generate_random_data()
            records.append({
                'Data': data.encode('utf-8')
            })
        
        try:
            response = self.firehose_client.put_record_batch(
                DeliveryStreamName=self.stream_name,
                Records=records
            )
            
            failed_count = response['FailedPutCount']
            success_count = count - failed_count
            
            print(f"✅ 배치 레코드 전송 완료")
            print(f"   성공: {success_count}개")
            print(f"   실패: {failed_count}개")
            print(f"   총 레코드: {count}개")
            
            if failed_count > 0:
                print("❌ 실패한 레코드:")
                for i, record_result in enumerate(response['RequestResponses']):
                    if 'ErrorCode' in record_result:
                        print(f"   레코드 {i+1}: {record_result['ErrorCode']} - {record_result['ErrorMessage']}")
            
            return success_count > 0
            
        except ClientError as e:
            print(f"❌ 배치 레코드 전송 실패: {e}")
            return False
    
    def send_custom_message(self, message):
        """사용자 정의 메시지 전송"""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp} - {message}\n"
        
        try:
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={
                    'Data': data.encode('utf-8')
                }
            )
            
            print(f"✅ 사용자 정의 메시지 전송 성공")
            print(f"   메시지: {message}")
            print(f"   RecordId: {response['RecordId']}")
            return True
            
        except ClientError as e:
            print(f"❌ 사용자 정의 메시지 전송 실패: {e}")
            return False
    
    def continuous_send(self, interval=5, duration=60):
        """지속적으로 데이터 전송 (테스트용)"""
        print(f"🔄 {duration}초 동안 {interval}초마다 데이터 전송 시작...")
        
        start_time = time.time()
        count = 0
        
        try:
            while time.time() - start_time < duration:
                if self.send_single_record():
                    count += 1
                    print(f"   진행률: {count}개 전송됨")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  사용자에 의해 중단됨 (총 {count}개 전송)")
        
        print(f"✅ 지속 전송 완료: 총 {count}개 레코드 전송")
        return count

def get_firehose_role_arn():
    """쉘 스크립트에서 생성한 Firehose IAM 역할 ARN 가져오기"""
    try:
        sts_client = boto3.client('sts')
        account_id = sts_client.get_caller_identity()['Account']
        role_name = "firehose-delivery-role"  # 쉘 스크립트에서 생성한 역할 이름
        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
        
        # 역할이 존재하는지 확인
        iam_client = boto3.client('iam')
        try:
            iam_client.get_role(RoleName=role_name)
            print(f"✅ Firehose IAM 역할 발견: {role_arn}")
            return role_arn
        except ClientError:
            print(f"⚠️  Firehose IAM 역할을 찾을 수 없음: {role_name}")
            return None
            
    except Exception as e:
        print(f"❌ IAM 역할 ARN 조회 실패: {e}")
        return None

def main():
    print("🚀 Kinesis Firehose 데이터 전송 테스트")
    print("=" * 40)
    
    # 스트림 이름 설정 (쉘 스크립트에서 생성한 이름과 일치해야 함)
    stream_name = "test-firehose-stream"
    
    # IAM 역할 ARN 자동 감지
    role_arn = get_firehose_role_arn()
    
    if role_arn:
        print("🔐 쉘 스크립트에서 생성한 IAM 역할을 사용합니다.")
        use_role = input("IAM 역할을 사용하시겠습니까? (Y/n): ").strip().lower()
        if use_role in ['', 'y', 'yes']:
            sender = FirehoseDataSender(stream_name, role_arn=role_arn)
        else:
            sender = FirehoseDataSender(stream_name)
    else:
        print("💡 기본 자격증명을 사용합니다.")
        sender = FirehoseDataSender(stream_name)
    
    while True:
        print("\n📋 메뉴를 선택하세요:")
        print("1. 단일 레코드 전송")
        print("2. 배치 레코드 전송 (5개)")
        print("3. 사용자 정의 메시지 전송")
        print("4. 지속적 전송 (60초간)")
        print("5. 종료")
        
        try:
            choice = input("\n선택 (1-5): ").strip()
            
            if choice == '1':
                sender.send_single_record()
                
            elif choice == '2':
                count = input("전송할 레코드 수 (기본값: 5): ").strip()
                count = int(count) if count else 5
                sender.send_batch_records(count)
                
            elif choice == '3':
                message = input("전송할 메시지를 입력하세요: ").strip()
                if message:
                    sender.send_custom_message(message)
                else:
                    print("❌ 메시지가 비어있습니다.")
                    
            elif choice == '4':
                interval = input("전송 간격(초, 기본값: 5): ").strip()
                duration = input("지속 시간(초, 기본값: 60): ").strip()
                
                interval = int(interval) if interval else 5
                duration = int(duration) if duration else 60
                
                sender.continuous_send(interval, duration)
                
            elif choice == '5':
                print("👋 프로그램을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다.")
                
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n\n👋 프로그램이 중단되었습니다.")
            break

if __name__ == "__main__":
    main()

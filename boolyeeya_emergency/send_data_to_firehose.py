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
                print(f"✅ Client BOOOM BOOOM ")
            else:
                self.firehose_client = boto3.client('firehose', region_name=region)
                print(f"✅ BASIC Client BOOOM BOOOM (리전: {region})")
                
        except NoCredentialsError:
            print("❌ NOOOO client.")
            exit(1)
        except ClientError as e:
            print(f"❌ No CRENDENTIAL FAILED WOOOO : {e}")
            print("💡 RE:RE:RE...")
            try:
                self.firehose_client = boto3.client('firehose', region_name=region)
                print(f"✅ BASIC Client BOOOM BOOOM")
            except Exception as fallback_error:
                print(f"❌ you are looser bitch: {fallback_error}")
                exit(1)
    
    def generate_random_data(self):
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
        if data is None:
            data = self.generate_random_data()
        
        try:
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={
                    'Data': data.encode('utf-8')
                }
            )
            
            print(f"✅ single record transport success")
            print(f"   RecordId: {response['RecordId']}")
            print(f"   sdize: {len(data)} bytes")
            print(f"   data: {data.strip()}")
            return True
            
        except ClientError as e:
            print(f"❌ fail wooooo: {e}")
            return False
    
    def send_batch_records(self, count=5):
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
            
            print(f"✅ batch record success")
            print(f"   success: {success_count}dog")
            print(f"   fail: {failed_count}dog")
            print(f"   total records: {count}dog")
            
            if failed_count > 0:
                print("❌ failed records:")
                for i, record_result in enumerate(response['RequestResponses']):
                    if 'ErrorCode' in record_result:
                        print(f"   records {i+1}: {record_result['ErrorCode']} - {record_result['ErrorMessage']}")
            
            return success_count > 0
            
        except ClientError as e:
            print(f"❌ Batch Record Failed woooo: {e}")
            return False
    
    def send_custom_message(self, message):
        timestamp = datetime.now().isoformat()
        data = f"{timestamp} - {message}\n"
        
        try:
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={
                    'Data': data.encode('utf-8')
                }
            )
            
            print(f"✅ Customized Data Transport Success")
            print(f"   messege: {message}")
            print(f"   RecordId: {response['RecordId']}")
            return True
            
        except ClientError as e:
            print(f"❌ Customized Data Transport failed wooo: {e}")
            return False
    
    def continuous_send(self, interval=5, duration=60):
        print(f"🔄 for {duration}s every {interval}s start data transport...")
        
        start_time = time.time()
        count = 0
        
        try:
            while time.time() - start_time < duration:
                if self.send_single_record():
                    count += 1
                    print(f"   about: {count}dog transport")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  shutdowned by you (total {count}dog transport)")
        
        print(f"✅ Complete: total {count}dog transport")
        return count

def get_firehose_role_arn():
    try:
        sts_client = boto3.client('sts')
        account_id = sts_client.get_caller_identity()['Account']
        role_name = "firefighter"  
        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
        
        # 역할이 존재하는지 확인
        iam_client = boto3.client('iam')
        try:
            iam_client.get_role(RoleName=role_name)
            print(f"✅ i found : {role_arn}")
            return role_arn
        except ClientError:
            print(f"⚠️  i cant found it: {role_name}")
            return None
            
    except Exception as e:
        print(f"❌ i cant found it woooo: {e}")
        return None

def main():
    print("🚀 Kinesis Firehose transport data test")
    print("=" * 40)
    
    # 스트림 이름 설정 (쉘 스크립트에서 생성한 이름과 일치해야 함)
    stream_name = "test-firehose-stream"
    
    # IAM 역할 ARN 자동 감지
    role_arn = get_firehose_role_arn()
    
    if role_arn:
        print("🔐 using the role made by you before.")
        use_role = input("using this role? coreectly? (Y/n): ").strip().lower()
        if use_role in ['', 'y', 'yes']:
            sender = FirehoseDataSender(stream_name, role_arn=role_arn)
        else:
            sender = FirehoseDataSender(stream_name)
    else:
        print("💡 using basic credentials.")
        sender = FirehoseDataSender(stream_name)
    
    while True:
        print("\n📋 choice fuck you:")
        print("1. single record post")
        print("2. batch record post (5dog)")
        print("3. customize record post")
        print("4. continous record post (for 60s)")
        print("5. exit")
        
        try:
            choice = input("\nchoice (1-5): ").strip()
            
            if choice == '1':
                sender.send_single_record()
                
            elif choice == '2':
                count = input("how many record do you post (default: 5): ").strip()
                count = int(count) if count else 5
                sender.send_batch_records(count)
                
            elif choice == '3':
                message = input("text it to post messages: ").strip()
                if message:
                    sender.send_custom_message(message)
                else:
                    print("❌ empty fuck you. write something")
                    
            elif choice == '4':
                interval = input("interval(seconds, default: 5): ").strip()
                duration = input("how long?(seconds, default: 60): ").strip()
                
                interval = int(interval) if interval else 5
                duration = int(duration) if duration else 60
                
                sender.continuous_send(interval, duration)
                
            elif choice == '5':
                print("👋 byebye.")
                break
                
            else:
                print("❌ wrong choices.")
                
        except ValueError:
            print("❌ input please inteager are you dumb ass?")
        except KeyboardInterrupt:
            print("\n\n👋 bye.")
            break

if __name__ == "__main__":
    main()

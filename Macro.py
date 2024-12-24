import time
from datetime import datetime
import requests

def get_server_time(server_url="https://ticket.melon.com/performance/index.htm?prodId=210649"):
    try:
        response = requests.get(server_url)
        response.raise_for_status()
        server_time = response.json().get("datetime")
        return datetime.fromisoformat(server_time[:-1])  # 'Z' 제거 후 파싱
    except Exception as e:
        print(f"서버 시간을 가져오는 데 실패했습니다: {e}")
        return None

def refresh_page(target_url):
    try:
        print("페이지 새로고침!")
        response = requests.get(target_url)
        response.raise_for_status()
        print(f"페이지 새로고침 성공: {response.status_code}")
    except Exception as e:
        print(f"페이지 새로고침 중 오류 발생: {e}")

def ticketing_macro(target_time_str, target_url):
    try:
        target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
        print(f"목표 시간: {target_time}")
        
        while True:
            server_time = get_server_time()
            if not server_time:
                print("서버 시간 동기화 실패, 로컬 시간 사용")
                server_time = datetime.now()

            print(f"현재 시간: {server_time}")
            if server_time >= target_time:
                refresh_page(target_url)
                break

            time.sleep(0.01)  # 루프 간격 조정 (10ms)
    except Exception as e:
        print(f"매크로 실행 중 오류가 발생했습니다: {e}")

# 실행 코드
if __name__ == "__main__":
    try:
        target_time_input = input("목표 시간을 입력하세요 (YYYY-MM-DD HH:MM:SS): ")
        target_url_input = input("새로고침할 URL을 입력하세요: ")
        ticketing_macro(target_time_input, target_url_input)
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")



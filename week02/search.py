import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "문화센터는 매주 월요일과 공휴일에는 운영하지 않는다.",
    "어린이 미술 교실은 토요일 오전 10시에 시작한다.",
    "요가 강좌는 한 달에 8번 진행된다.",
    "공연장은 최대 200명까지 입장할 수 있다.",
    "악기 대여는 회원만 무료로 이용할 수 있다.",
    "전시실에서는 사진 촬영이 금지되어 있다.",
    "여름 특별 프로그램 접수는 6월 첫째 주부터 시작된다.",
    "카페는 1층 로비 옆에 위치해 있다.",
    "자원봉사자는 활동 시간을 확인받아야 한다.",
    "강의실 예약은 인터넷으로만 신청할 수 있다.",
]
D = np.stack([emb(d) for d in docs])          # 문서 10개를 미리 벡터로 (10 x 1024)

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))   # 문서 10개와의 코사인을 한 번에
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")

for question in ["한 주 동안 쉬는 날은 언제인가요?", "악기를 비용 없이 빌릴 수 있는 사람은 누구인가요?", "학교 그만두려면 어떻게 해?",
                 "수업 공간을 이용하려면 어떤 방식으로 절차를 진행해야 하나요?"]:
    print("Q:", question)
    search(question)
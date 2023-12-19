**1.루빅스 트래블 게임 GUI 구현**

이 게임 파일은 총 3개입니다.

rubiksFlipTravel.py
minimax.py
evaluate.py


rubiksFlipTravel.py
- v2 ai_move에서 depth=4 도 추가하여 더 깊은 depth를 한 개 더 탐색. 그리하여 좀 더 많은 경우의 보드를 scoring할 수 있음.
- v3 info_ai_message 추가 - ai가 수를 두면  gui화면 보드 상단에 경과시간, depth를 출력하는 메서드 추가
- v3 cant_move 메서드 추가 - 현재 보드 상황을 탐색하여, 상대의 타일을 옮길 차례일 때 옮길 수 있는 타일이 있는지 검사하는 메서드. 있으면 False 없으면 True를 리턴




minimax.py
- v2 evaluate메서드를 실행해서 scoring 하는 조건을 추가.  보드의 승리 조건도 넣어서 보드가 어느 플레이어의 승리 상황이던 평가함수를 작동하게 하고 승리자에 맞는 점수를 리턴함.



evaluate.py
- v1.1 기존 코드 주석 정리
- v2 EDGE_SCORE 을 95점으로 하양하여 전체적인 밸런스 조절



**2.버팔로 체스 게임 GUI 구현**

이 게임 파일은 총 4개입니다
buffalo_chess_piece.py-최준석 제출
buffalo_chess_team.py-정영균 제출
buffalo_chess_display.py-임준우 제출
buffalo_chess_main.py-박규성 제출


-buffalo_chess_piece.py
이 파일은 버팔로 체스에서 체스말의 정보를 나타냅니다.


-buffalo_chess_team.py
이 파일은 버팔로 체스에서 각 팀의 정보를 나타냅니다.

-buffalo_chess_display.py
이 파일은 버팔로 체스를 GUI로 구현하기 위한 창 정보와 디스플레이의 정보를 담고 있습니다

-buffalo_chess_main.py
이 파일은 버팔로 체스의 현재 보드판의 정보와 체스말을 클릭하면 이동가능한 모든 칸을 나타내는 함수, 체스말을 이동시키는 함수 등 게임에 대한 함수와 ai의 차례일때 보드판의 평가 점수에 따라 최적의 수를 두는 ai 함수, 순서에 따라 게임을 실행하는 메인 함수를 담고 있는 파일입니다.


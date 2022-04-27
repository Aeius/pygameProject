# pygameProject

1. 기획

  1) 점프해서 무한히 올라가는 두들 점프게임 구현
  2) 캐릭터는 좌,우 움직임 및 점프 하면서 움직임
  3) 플랫폼을 따라서 점프해서 올라가야함
  4) 점수획득 방식
      1. 플랫폼을 밟는다(1회만 점수 적용)
      2. 높은 위치로 올라가 아래쪽 플랫폼이 사라진다.
      3. 코인을 획득한다.
  5) 게임오버 규칙
      1. 제한시간 종료
      2. 캐릭터가 바닥아래로 추락
  6) 메인화면에서 난이도 조절 가능
  7) 난이도는 총 3가지(easy, nomal, hard) - 난이도의 따른 플랫폼 길이 조절
  8) 최고점수 출력 및 갱신 
  9) BGM 및 효과음 출력
  
2. 구현

- 메인화면에서 난이도 설정 가능

https://user-images.githubusercontent.com/87006912/165521523-42372733-1e46-4826-bdb4-b4dc7ebcf445.mp4


 - 캐릭터 이동, 점프 및 배경음 효과음 출력
https://user-images.githubusercontent.com/87006912/165521156-bf7393cb-581c-486c-8685-5647b1d7adf8.mp4


- 땅에 떨어지면 게임 오버 게임오버 됨과 동시에 점수 및 최고 점수 출력

https://user-images.githubusercontent.com/87006912/165521627-cc2fc96d-eee7-45a8-8721-c1bd52dc6ae4.mp4


- 제한 시간이 초과되면 게임오버

https://user-images.githubusercontent.com/87006912/165521936-45997ff0-2174-4c9c-8905-1d85e5387e33.mp4


- 플랫폼을 밟을 시 점수 100점 증가 (1회 한정)

https://user-images.githubusercontent.com/87006912/165522498-d4afb0c4-74c2-4bb3-983d-3cb0e66830d7.mp4


- 코인 획득 시 점수 1점 증가 (코인은 멈춰있는 발판에만 생성됨)

https://user-images.githubusercontent.com/87006912/165522701-2cf178d4-540a-49db-be94-85644c8d0b6f.mp4



- 플레이 영상 및 전체 설명

https://user-images.githubusercontent.com/87006912/165523047-1896354e-94de-45b3-b561-f875bd201d58.mp4



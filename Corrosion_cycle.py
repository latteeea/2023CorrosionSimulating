import random
import math
import matplotlib.pyplot as plt
import numpy as np

# 기준면적 : area(i값), 델타x(사이클) : cycle, 
# 반지름 리스트 : r, 갯수 리스트 : n, 배율 : m, K1, Kn, del_K
# 반복횟수 : times 으로 input


# 그래프 그리는 함수
def drawCircle(area, circle):
    
    totalcenter = []
    totalradius = []

    
    for i in range(len(circle)):
        totalcenter.append([circle[i][0], circle[i][1]])
        totalradius.append(circle[i][2])
    
    for center, radius in zip(totalcenter,totalradius):
        circle = plt.Circle(center, radius, color='blue', fill=True)
        plt.gca().add_patch(circle)

    plt.axis('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Circles')
    plt.xticks(np.arange(-20,area+20,10))
    plt.yticks(np.arange(-20,area+20,10))
    plt.axis([-20,area+20, -20, area+20])

    plt.hlines(0,0,area,color='red', linestyle='solid',linewidth=2)
    plt.hlines(area,0,area,color='red', linestyle='solid',linewidth=2)
    plt.vlines(0,0,area,color='red', linestyle='solid',linewidth=2)
    plt.vlines(area,0,area,color='red', linestyle='solid',linewidth=2)
    plt.grid()
    plt.show()
    

# 결함들에 대한 정보가 바뀔 때마다 갱신하는 함수
def newCircle(total_circle_xy, circle_r, first_cycle):
    circle = {}
    for i in range(len(circle_r)):
        circle[i] = total_circle_xy[i].copy()
        circle[i].append(circle_r[i])
        circle[i].append(first_cycle[i])
        
    return circle
    
    
# 결함 간의 최단거리 계산
def min_distance(x1,y1,x2,y2,r1,r2):
    tmp = (x1-x2)**2 + (y1-y2)**2
    distance = math.sqrt(tmp)
    min_d = distance - r1 - r2
    return round(min_d, 3)


# 면적율 (area_ratio) 함수 (K와 비교대상)
def area_ratio(area,circle):
    sum = 0
    for i in range(len(circle)):
        x = circle[i][0]
        r = circle[i][2]
        eachSum = (r * r) * 3.14
        if ((area - x) < r):   # 면적 벗어났을 때
            ceta = math.acos((area-x)/r)
            ceta = math.degrees(ceta)
            eachSum = eachSum - ((ceta/180 * 3.14 * r*r) - ((area - x) * r))
        sum += eachSum
    
    area_ratio = round((sum / (area*area)) * 100, 3)
    return area_ratio


# 두 결함이 결합해서 나온 새로운 결함의 [x,y,반지름,사이클] 리스트
def comb(a, b, x0, y0, m, r1, r2, x1, x2, y1, y2, cycle):
    area = (r1*r1*3.14 + r2*r2*3.14)*m
    r = round(math.sqrt(area/3.14),3)
    x = round((r1*x1 + r2*x2) / (r1 + r2), 3)
    y = round((r1*y1 + r2*y2) / (r1 + r2), 3)
    tmp_cycle = round(x0 - (b * (math.log((a / (r-y0)) - 1))), 3)
    tmp_cycle = round(tmp_cycle - cycle,3)
    result = [x,y,r,tmp_cycle]
    return result


# 해당 사이클의 결함 반지름 계산 함수 (tmp_r : 결함의 반지름)
def r_cycle(a,b,x0,y0,cycle):
    # tmp_r = a/(1+(math.pow((math.e), (-cycle+x0)/b)))
    tmp_r = y0 + a / (1 + np.exp((-(cycle - x0)) / b))
    return round(tmp_r, 3)



# 초기정보 입력
print("초기정보를 입력하세요\n")
area = int(input("기준면적(i의 값): "))
# cycle = int(input("델타사이클: "))
min_d = float(input("결함 최소 거리: "))
a = float(input("상수 a: "))
b = float(input("상수 b: "))
x0 = float(input("X0 상수: "))
y0 = float(input("y0 상수: "))
r = list(map(float, input("원형결함의 반지름(띄어쓰기 구분): ").split(" ")))
n = list(map(int, input("원형결함의 갯수(띄어쓰기 구분): ").split(" ")))
m = float(input("배율: "))
times = int(input("반복횟수: "))
Cycle = list(map(int, input("원하는 사이클(띄어쓰기 구분): ").split(" ")))


# 추가적으로 필요한 변수

n_circle = 0
for i in range(len(n)):
    n_circle += n[i]         #총 원형 결함의 갯수 (2,2,1 이면 5개)
    
    
circle_r = []   #ex) [0.5,0.5,1.0,1.0,1.5]

for i in range(len(n)):          # 케이스 끝나도 불변
    n_n = n[i]   
    r_r = r[i]   
    
    while(n_n > 0):
        circle_r.append(r_r)
        n_n = n_n - 1
        
        

for ss in range (1, times+1): # if 첫번째 케이스일때랑 그 다음일때 나눠서 써야할듯 (for 문 안에다가 집어넣긴 하지만)
    cycle = Cycle.copy()

    print("========================================")

  
    t = 0

    while (len(cycle) >= 1):        # 하나의 케이스가 끝날 때까지
        
        if (t == 0):
    
            circle_x = []
            circle_y = []
            total_circle_xy = []  #이차원 리스트
            
            circle_r = []   #ex) [0.5,0.5,1.0,1.0,1.5]

            for i in range(len(n)):
                n_n = n[i]   
                r_r = r[i]   
                
                while(n_n > 0):
                    circle_r.append(r_r)
                    n_n = n_n - 1


            # 면적 내 좌표에 랜덤 분포한 결함의 좌표(원의 중심의 x,y 좌표)
            for i in range(n_circle):
                x = round(random.uniform(0,area), 3)
                y = round(random.uniform(0,area), 3)
                circle_x.append(x)
                circle_y.append(y)
                total_circle_xy.append([circle_x[i],circle_y[i]])
                
                
            # 각 결함에 대한 정보 dictionary 생성(초기)
            circle = {}
            for i in range(n_circle):
                circle[i] = total_circle_xy[i].copy()
                circle[i].append(circle_r[i])
            

            areaRatio = area_ratio(area,circle)
        
            

            # 성장 시작 지점 (반지름별 초기 사이클값) 구하기 
            for i in range(len(circle)):
                tmp = round((a / (circle[i][2])) - 1, 3)
                # print("tmp=", tmp)
                first = round((x0 - b * math.log((a / ((circle[i][2])-y0)) - 1)), 3)
                circle[i].append(first)
                

            first_cycle = []     # 초기 사이클 리스트
            for i in range(len(circle)):
                first_cycle.append(circle[i][3])

            print(ss,"번째 초기 결함 정보 =", circle)
                        
            error = []   #초기에 겹쳐진 결함 번호 리스트

            # 초기에 겹쳐진 결함이 있는 경우 (min_d <= 0 일 때)
            for i in range(len(circle)):
                for j in range(i+1,len(circle)):
                    if ((min_distance(circle[i][0], circle[i][1], circle[j][0], circle[j][1], circle[i][2], circle[j][2])) <= 0):
                        error.append([i,j])  

            if (len(error) > 0):    #결합
                for i in range(len(error)):
                    a = error[i][0]
                    b = error[i][1]
                    circle[a] = comb(a, b, x0, m, circle[a][2], circle[b][2], circle[a][0], circle[b][0], circle[a][1], circle[b][2], cycle[0])
                    del total_circle_xy[b]
                    del circle_r[b]
                    del first_cycle[b]
                    total_circle_xy[a] = [(circle[a][0]),(circle[a][1])]
                    
                    circle_r[aa] = circle[aa][2]
            
                    for u in range(len(circle_r)):
                        circle_r[u] = circle[u][2]
                        
                    first_cycle[a] = circle[a][3]
                    circle = newCircle(total_circle_xy, circle_r, first_cycle)    
                    del error[0]
            else:
                pass
                
            drawCircle(area, circle)   

            output = {}    # 최종적으로 구하려는 결과값


    
        else :          # 하나의 케이스에서 두번째 경우 이상일 때
            
            newCycle = cycle[0]
            circle1 = {}      # 결함의 반지름만 나오는 dictionary
            
            for j in range(len(circle)):      # j는 circle key
                thisCycle = circle[j][3] + newCycle
                # print("thisCycle =",thisCycle)
                circle[j][2] = r_cycle(a,b,x0,y0,thisCycle)     # 사이클에 맞는 반지름 구함
                circle1[j] = circle[j][2]

            if (len(circle) > 1):
                for k in range(len(circle)):     # 결합 조건에 부합할 때
                    for p in range(k+1, len(circle)):
                        if (min_distance(circle[k][0], circle[k][1], circle[p][0], circle[p][1], circle[k][2], circle[p][2]) <= min_d):
                            error.append([k,p])

            # print("========",i,"번째 ==========")
            # print("circle1 = ", circle1)

          
            if (len(error) >= 1):
                if (len(error) > 1):
                    min_d_list = []
                    for s in range(len(error)):
                        min_d_list.append(min_distance(circle[(error[s][0])][0], circle[(error[s][0])][1], circle[(error[s][1])][0], circle[(error[s][1])][1], circle[(error[s][0])][2], circle[(error[s][1])][2]))
                    q = min_d_list.index(min(min_d_list))
                    aa = error[q][0]
                    bb = error[q][1]
                        
                elif(len(error) == 1):
                    aa = error[0][0]
                    bb = error[0][1]
                
                
                try: 
                    circle[aa] = comb(a, b, x0, y0, m, circle[aa][2], circle[bb][2], circle[aa][0], circle[bb][0], circle[aa][1], circle[bb][1], cycle[0])
                    
                except ValueError:
                    print("log의 값이 음수가 되어 더 이상 cycle을 측정할 수 없습니다")       #cycle에 대한 결함 반지름 구할 때 로그함수가 쓰이는데, 이때 음수가 나오면 더이상 측정 불가
                    print(ss,"번째 output =",output)
                    break
                
                del total_circle_xy[bb]
                del circle_r[bb]
                del first_cycle[bb]
                total_circle_xy[aa] = [(circle[aa][0]),(circle[aa][1])]
                circle_r[aa] = circle[aa][2]
            
                    
                for u in range(len(circle_r)):
                    circle_r[u] = circle[u][2]
                    

                first_cycle[aa] = circle[aa][3]
                circle = newCircle(total_circle_xy, circle_r, first_cycle)   

                
            error = []
            

            drawCircle(area, circle)
            print("사이클: ", cycle[0], end = ", ")
            print("현재 면적율: ", area_ratio(area,circle))

                        
        t = t + 1
        
        del cycle[0]

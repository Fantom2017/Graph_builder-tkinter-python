from tkinter.ttk import Combobox
import turtle
from tkinter import *
from tkinter import filedialog
from math import *
from copy import*
from time import*
from collections import deque
from heapq import heappush, heappop


def move(x, y):
    alex.penup()
    alex.goto(x, y)
    alex.pendown()


def Check_num(x, y):
    global click_num, mas
    i = 0
    num = 0
    while i < mas[2] - 1 and num == 0:
        if (abs(x - mas[0][i * 2]) < size * 2) and (abs(y + size - mas[0][i * 2 + 1]) < size * 2):
            num = i + 1
        i += 1
    return num


def dot(mas, size, color, x, y, N):
    move(x, y)
    alex.fillcolor(color)
    alex.begin_fill()
    alex.circle(size)
    move(x, y + size / 2)
    alex.pencolor('black')
    alex.write(N)
    alex.pencolor(color)
    alex.end_fill()


def DrawGraph(mas, color, size):
    for j in range(len(mas[1])):
        for k in range(len(mas[1][j])):
            if mas[1][j][k] == 1:
                draw_edge(mas, j + 1, k + 1)
    for i in range((len(mas[0])) // 2):
        dot(mas, size, color, mas[0][i * 2], mas[0][i * 2 + 1] - size, i + 1)


def delete_dot(mas, x, y):
    num = Check_num(x, y)
    for i in range(mas[2] - 1):
        if mas[1][num - 1][i - 1] == 1:
            delete_edge(mas, num, i)
    alex.pencolor('white')
    move(mas[0][num * 2 - 2] - size, mas[0][num * 2 - 1] + size)
    alex.fillcolor('white')
    alex.begin_fill()
    for i in range(4):
        alex.forward(size * 2)
        alex.right(90)
    alex.end_fill()
    mas[0].pop(num * 2 - 1)
    mas[0].pop(num * 2 - 2)
    mas[1].pop(num - 1)
    for i in range(mas[2] - 2):
        mas[1][i].pop(num - 1)
    mas[2] -= 1
    alex.pencolor(color)
    for i in range(num, mas[2]):
        dot(mas, size, color, mas[0][i * 2 - 2], mas[0][i * 2 - 1] - size, i)


def delete_dot_from_list(mas, x, y):
    i = mas[0].index(x)
    j = mas[0].index(y)
    j_idx = j // 2
    mas[0].pop(j)
    mas[0].pop(i)
    for k in range(mas[2]):
        mas[1][j_idx][k] = 0
        mas[1][k][j_idx] = 0
    mas[2] -= 1
    del mas[1][j_idx]
    del mas[1][i // 2]


def delete_edge_from_list(mas, n1, n2):
    mas[1][n1 - 1][n2 - 1] = 0
    mas[1][n2 - 1][n1 - 1] = 0

def draw_edge(mas, n1, n2):
    move(mas[0][n1 * 2 - 2], mas[0][n1 * 2 - 1])
    alex.goto(mas[0][n2 * 2 - 2], mas[0][n2 * 2 - 1])
    mas[1][n1 - 1][n2 - 1] = 1
    mas[1][n2 - 1][n1 - 1] = 1


def delete_edge(mas, n1, n2):
    move(mas[0][n1 * 2 - 2], mas[0][n1 * 2 - 1])
    alex.pencolor('white')
    alex.goto(mas[0][n2 * 2 - 2], mas[0][n2 * 2 - 1])
    mas[1][n1 - 1][n2 - 1] = 0
    mas[1][n2 - 1][n1 - 1] = 0
    alex.pencolor('orange')
    dot(mas, size, color, mas[0][n1 * 2 - 2], mas[0][n1 * 2 - 1] - size, n1)
    dot(mas, size, color, mas[0][n2 * 2 - 2], mas[0][n2 * 2 - 1] - size, n2)


def reset(mas, color, size):
    mas = [mas[0], mas[1], N]
    move(-500, -500)
    alex.fillcolor('white')
    alex.begin_fill()
    for i in range(4):
        alex.forward(1000)
        alex.left(90)
    alex.end_fill()
    DrawGraph(mas, color, size)


def exit_file():
    turtle.Screen().bye()
    root.destroy()


def save_file(mas):
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    text = str(mas)
    with open(filename, "w") as file:
        file.write(text)


def open_file():
    global color, size, mas
    move(-500, -500)
    alex.fillcolor('white')
    alex.begin_fill()
    for i in range(4):
        alex.forward(1000)
        alex.left(90)
    alex.end_fill()
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        file_txt = file.read()
    check = file_txt
    check1 = check[check.find('[', 1) + 1:check.find(']')]
    check1 = check1.replace(' ', '')
    check1 = check1.split(',')
    for i in range(len(check1)):
        check1[i] = float(check1[i])
    check = check[check.find(']') + 3:]
    N = file_txt[-3:-1]
    N = int(N)
    check2 = check[:-6]
    check2 = check2.replace('[', '')
    check2 = check2.replace(']', '')
    check2 = check2.replace(' ', '')
    check2 = check2.split(',')
    a = []
    for i in range(len(check2)):
        check2[i] = int(check2[i])
    for i in range(round((sqrt(len(check2))))):
        a = a + [check2[i * (N - 1):(i + 1) * (N - 1)]]
    check2 = a
    mas = [check1] + [check2] + [N]
    DrawGraph(mas, color, size)


def DFS(N, mas):
    stack = [N]
    visited = [False] * mas[2]
    visited[N-1] = True
    check = [N]
    dot(mas, size, 'green', mas[0][N * 2 - 2], mas[0][N * 2 - 1] - size, N)
    sleep(1)
    while len(stack) != 0:
        current = stack[-1]
        found_next = False
        for i in range(mas[2]-1):
            if mas[1][current-1][i] == 1:
                if not visited[i]:
                    stack.append(i+1)
                    visited[i] = True
                    check += [i+1]
                    dot(mas, size, 'green', mas[0][i * 2], mas[0][i * 2 + 1] - size, i+1)
                    sleep(1)
                    found_next = True
                    break
        if not found_next:
            stack.pop()
            dot(mas, size, 'purple', mas[0][current * 2 - 2], mas[0][current * 2 -1] - size, current)
            sleep(1)

    if set(check) == set(range(1, mas[2])):
        move(-350, 270)
        alex.write("Граф зв'язаний", font=(20))
    else:
        move(-350, 270)
        alex.write("Граф не зв'язаний", font=(20))
    alex.pencolor(color)

         
def BFS(N, mas):
    check = [N]
    queue = [N] 
    var = True
    visited = [False] * mas[2]
    visited[N-1] = True
    dot(mas, size, 'green', mas[0][N * 2 - 2], mas[0][N * 2 - 1] - size, N)
    while len(queue) != 0:
        for i in range(mas[2]-1):
            if mas[1][queue[0]-1][i] == 1:
                if not visited[i]:
                    queue += [i+1] 
                    check += [i+1]
                    visited[i] = True
                    dot(mas, size, 'green', mas[0][i * 2], mas[0][i * 2 + 1] - size, i+1)         
        dot(mas, size, 'purple', mas[0][queue[0] * 2 - 2], mas[0][queue[0] * 2 -1] - size, queue[0])       
        queue = queue[1:]
        sleep(1)  

    if set(check) == set(range(1, mas[2])):
        move(-350, 270)
        alex.write("Граф зв'язаний", font=(20))
    else:
        move(-350, 270)
        alex.write("Граф не зв'язаний", font=(20))
    alex.pencolor(color)
         

def dijkstra(num1, num2, mas):
    distances = [float('inf')] * mas[2]
    distances[num1 - 1] = 0
    visited = [False] * mas[2]
    path = [-1] * mas[2]

    for i in range(mas[2]-1):
        min_dist = float('inf')
        for j in range(mas[2]-1):
            if not visited[j] and distances[j] < min_dist:
                min_dist = distances[j]
                curr = j
        visited[curr] = True
        for j in range(mas[2]-1):
            if mas[1][curr][j] == 1:
                if distances[curr] + 1 < distances[j]:
                    distances[j] = distances[curr] + 1
                    path[j] = curr

        dot(mas, size, 'green', mas[0][curr * 2], mas[0][curr * 2 + 1] - size, curr + 1)
        sleep(1)

        if curr + 1 == num2:
            break

    if path[num2 - 1] == -1:
        print('0')
    else:
        res = []
        curr = num2 - 1
        while curr != -1:
            res.append(curr + 1)
            curr = path[curr]
    move(-350, 270)
    alex.write(res[::-1], font=(20))


def Eulerian_path(mas):
    var = True
    count = 0
    for i in range(mas[2]-1):
        if (mas[1][i].count(1)) % 2 != 0:
            count += 1
    if count > 2:
        move(-350, 270)
        alex.write("Нема ейлеревих шляхів", font=(20))
    else:
        mas_copy = deepcopy(mas)
        degrees = [0] * mas_copy[2]
        for i in range(mas_copy[2] - 1):
            for j in range(mas_copy[2] - 1):
                if mas_copy[1][i][j] == 1:
                    degrees[i] += 1
        
        start_vertex = 0
        for i in range(mas[2] - 1):
            if degrees[i] % 2 == 1:
                start_vertex = i
                break
        
        stack = [start_vertex]
        path = []
        while len(stack) != 0:
            current = stack[-1]
            found_next = False
            dot(mas, size, 'green', mas[0][start_vertex * 2], mas[0][start_vertex * 2 + 1] - size, start_vertex+1)
            for i in range(mas[2] - 1):
                if mas_copy[1][current][i] == 1 and degrees[current] > 0:
                    
                    degrees[current] -= 1
                    degrees[i] -= 1
                    mas_copy[1][current][i] = 0
                    mas_copy[1][i][current] = 0
                    stack.append(i)
                    found_next = True
                    break
                
            if not found_next:
                path.append(stack.pop() + 1)
                dot(mas, size, 'purple', mas[0][current * 2], mas[0][current * 2 + 1] - size, current + 1)
        
        path.reverse()
        move(-350, 270)
        alex.write(path, font=(20))


def draw_left(x, y):
    global N, click_num, click, click_save, temp_x, temp_y, num_save, mas, num1
    if tools.get() == 'draw':
        var = True
        click += 1
        click_num = 1
        if mas[2] > 1:
            i = 0
            while (i < mas[2] - 1) and (var == True):
                if (abs(x - mas[0][i * 2]) < size * 3) and (abs(y + size - mas[0][i * 2 + 1]) < size * 3):
                    var = False
                i += 1
            if var:
                move(x, y)
                dot(mas, size, color, x, y, mas[2])
                mas[2] += 1
                click_num += 1
                mas[0] += [x] + [y + size]
                for i in range(mas[2] - 2):
                    mas[1][i].append(0)
                mas[1].append([])
                for i in range(mas[2] - 1):
                    mas[1][mas[2] - 2].append(0)

        else:
            move(x, y)
            dot(mas, size, color, x, y, mas[2])
            mas[2] += 1
            mas[0] += [x] + [y + size]
            click_num += 1
            mas[1][0].append(0)

        num = Check_num(x, y)

        if click_num == 1:
            if Check_num(x, y) == num_save and click_save == click - 1:
                delete_dot(mas, x, y)
                temp_x = 0
                temp_y = 0
                click_save = 0
            elif click_save == click - 1 and Check_num(x, y) != num_save:
                num = Check_num(x, y)
                if mas[1][num - 1][num_save - 1] == 1:
                    delete_edge(mas, num, num_save)
                else:
                    draw_edge(mas, num, num_save)
                click_save = 0
                num_save = 0
            else:
                click_save = click
                num_save = Check_num(x, y)
    elif tools.get() == 'DFS':
        click_num = 1
        i = 0
        var = True
        while (i < mas[2] - 1) and (var == True):
            if (abs(x - mas[0][i * 2]) < size * 3) and (abs(y + size - mas[0][i * 2 + 1]) < size * 3):
                var = False
            i += 1
        if var:
            click_num += 1
        if click_num == 1:
            DFS(Check_num(x, y), mas)
    elif tools.get() == 'BFS':
        click_num = 1
        i = 0
        var = True
        while (i < mas[2] - 1) and (var == True):
            if (abs(x - mas[0][i * 2]) < size * 3) and (abs(y + size - mas[0][i * 2 + 1]) < size * 3):
                var = False
            i += 1
        if var:
            click_num += 1
        if click_num == 1:
            BFS(Check_num(x, y), mas)
    elif tools.get() == 'Eulerian path':
        click_num = 1
        i = 0
        var = True
        while (i < mas[2] - 1) and (var == True):
            if (abs(x - mas[0][i * 2]) < size * 3) and (abs(y + size - mas[0][i * 2 + 1]) < size * 3):
                var = False
            i += 1
        if var:
            click_num += 1
        if click_num == 1:
            Eulerian_path(mas)
    elif tools.get() == 'Dijkstra':
        click_num = 1
        i = 0
        var = True
        while (i < mas[2] - 1) and (var == True):
            if (abs(x - mas[0][i * 2]) < size * 3) and (abs(y + size - mas[0][i * 2 + 1]) < size * 3):
                var = False
            i += 1
        if var:
            click_num += 1
        if click_num == 1 and num1 == 0:
            num1 = Check_num(x, y)
        elif click_num == 1 and num1 != 0: 
            num2 =Check_num(x, y)
            dijkstra(num1, num2, mas)

            

        



N = 1
color = '#FF8000'
size = 25
click = 0
coordinates = []
connection = [[]]
click_save = 0
temp_x = 0
temp_y = 0
num_save = 0
num1 = 0
mas = [coordinates, connection, N]
tools_list = ['draw', 'DFS', 'BFS', 'Eulerian path', 'Dijkstra']
root = Tk()
root.geometry('800x650')
root.config(bg='white')
canvas = Canvas(root, width=800, height=630)
screen = turtle.TurtleScreen(canvas)
alex = turtle.RawTurtle(screen)
alex.pencolor(color)
alex.speed(0)
res = Button(root, text='reset', command=lambda: reset(mas, color, size))
open_file_button = Button(root, text='open', command=lambda: open_file())
exit_button = Button(root, text='exit', command=lambda: exit_file())
save_file_button = Button(root, text='save', command=lambda: save_file(mas))
tools = Combobox(root, values=tools_list)
tools.current(0)
res.place(relx=0, rely=0, relheight=0.03, relwidth=0.05)
open_file_button.place(relx=0.05, rely=0, relheight=0.03, relwidth=0.05)
exit_button.place(relx=0.1, rely=0, relheight=0.03, relwidth=0.05)
save_file_button.place(relx=0.15, rely=0, relheight=0.03, relwidth=0.05)
tools.place(relx=0.2, rely=0, relheight=0.03, relwidth=0.1)
canvas.place(relx=0, rely=0.03)
screen.onscreenclick(draw_left, 1)
mainloop()   
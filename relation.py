A = [1, 2, 3, 4, 5]
N = len(A)


def read_matrix():
    matrix = []
    for i in range(N):
        while True:
            row = input(f'{i+1}행 (0/1을 공백으로 구분): ').split()
            if len(row) == N and all(x in ('0', '1') for x in row):
                matrix.append(list(map(int, row)))
                break
            print('오류: 0 또는 1을 정확히 5개 입력하세요.')
    return matrix


def show_matrix(matrix):
    for row in matrix:
        print(*row)


def is_reflexive(m):
    return all(m[i][i] == 1 for i in range(N))


def is_symmetric(m):
    return all(m[i][j] == m[j][i]
               for i in range(N) for j in range(N))


def is_transitive(m):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if m[i][j] and m[j][k] and not m[i][k]:
                    return False
    return True


def check_relation(m):
    results = [is_reflexive(m), is_symmetric(m), is_transitive(m)]
    for name, result in zip(['반사', '대칭', '추이'], results):
        print(f'{name} 관계: {"O" if result else "X"}')
    print('동치 관계입니다.' if all(results) else '동치 관계가 아닙니다.')
    return all(results)


def equivalence_class(m, i):
    return [A[j] for j in range(N) if m[i][j] == 1]


def show_classes(m):
    for i in range(N):
        members = ', '.join(map(str, equivalence_class(m, i)))
        print(f'[{A[i]}] = {{{members}}}')
    # 추가 기능: 중복 없는 분할 출력
    groups = []
    for i in range(N):
        group = equivalence_class(m, i)
        if group not in groups:
            groups.append(group)
    print('집합의 분할:', groups)
    print('서로 다른 동치류 개수:', len(groups))


def reflexive_closure(m):
    c = [row[:] for row in m]
    for i in range(N):
        c[i][i] = 1
    return c


def symmetric_closure(m):
    c = [row[:] for row in m]
    for i in range(N):
        for j in range(N):
            if m[i][j] == 1:
                c[j][i] = 1
    return c


def transitive_closure(m):
    c = [row[:] for row in m]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if c[i][k] and c[k][j]:
                    c[i][j] = 1
    return c


def main():
    print('=== 관계 행렬 분석 프로그램 ===')
    m = read_matrix()
    print('\n[입력 행렬]')
    show_matrix(m)
    print('\n[최초 판별]')
    if check_relation(m):
        show_classes(m)
        return
    steps = [('반사', is_reflexive, reflexive_closure),
             ('대칭', is_symmetric, symmetric_closure),
             ('추이', is_transitive, transitive_closure)]
    for name, check, closure in steps:
        if not check(m):
            print(f'\n[{name} 폐포 변환 전]')
            show_matrix(m)
            c = closure(m)
            print(f'[{name} 폐포 변환 후]')
            show_matrix(c)
            m = c
        else:
            print(f'\n{ name } 관계 충족: 변환 생략')
    print('\n[최종 판별]')
    if check_relation(m):
        show_classes(m)


if __name__ == '__main__':
    main()

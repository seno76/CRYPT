    # p, b, Q, r  = gen_curve(6, 10)
    # print(f"Была сгенерирована следующая кривая: p = {p}, B = {b}, (x0, y0) = {Q}, r = {r}")
    # # Параметры эллиптической кривой
    # k = 10
    # a = 0   # коэффициент a эллиптической кривой
    # l, P = gen_P(Q, p, a, b)
    # print("--------------------------", l, P)
    # write_l(l, P)
    # print(l, P, curve.mul_scalar_(l, Q[0], Q[1], p))
    # for i in range(k):
    #     input()
    #     l, P = read_l()
    #     print("--------------------------", l, P)
    #     step_1(Q, P, l, r)
        
    #     R = read_R()
    #     step_2(r, R, p)

    #     bit = read_bit()
    #     step_3(bit)

    #     print(f"{i + 1}) Проверка:", step_4(R, Q, P, p))
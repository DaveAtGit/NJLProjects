from sympy import *
import math
import cairo


class LogoConstructor:
    # props
    angle_alpha = 30
    sin_a = abs(math.sin(math.radians(angle_alpha)))
    cos_a = abs(math.cos(math.radians(angle_alpha)))
    tan_a = abs(math.tan(math.radians(angle_alpha)))

    def draw_logo(self, radius):
        # trigonometry
        sin_a = self.sin_a
        cos_a = self.cos_a
        tan_a = self.tan_a

        # dimensions:
        x_scale = y_scale = radius * 2
        x_center = y_center = radius
        hex_width = radius * cos_a
        # hexagon, area:
        area_hexagon = 6 * math.pow(1, 2) * math.sqrt(3) / 4
        area_each_shape = area_hexagon / 3

        # vars:
        ln_x, ln_v = symbols('x v', real=True)
        # determined, todo: x, v as dynamic vars
        ln_x = 0.31
        ln_v = 0.19
        ln_y = cos_a - ln_x
        ln_w = cos_a - ln_v

        # calc  the lines
        def shape_calculator():
            """
            define L-, J- and N-shapes, then calculate the vertical lines of l2, n4 and j3
            to get equal value for all three areas
            :return: all vertical lines from the L-, J- and N-shapes
            """
            ln_l2y, ln_j3y, ln_n4y = symbols('l2 j3 n4', real=True)

            # L-Part
            ln_l1 = ln_y * tan_a
            L_1 = ln_y * ln_l1
            ln_l3 = ln_v * tan_a
            L_3 = ln_v * ln_l3
            ln_l5 = ln_w * tan_a
            L_5 = ln_w * ln_l5
            print("check l5_y: ", ln_l5)
            ln_l4 = (ln_w - ln_v * tan_a)
            L_4 = ln_v * ln_l4
            print("check l4_y: ", ln_l4)
            L_2 = ln_l2y * ln_y
            L_total = Eq(L_1 + L_2 + L_3 + L_4 + L_5, area_each_shape)
            res_L = solve(L_total, ln_l2y)
            print("to solve l2_y: ", res_L[0])
            ln_l2 = res_L[0]
            # print("recheck l2:", ln_l2)

            # N-Part
            ln_n1 = ln_x * tan_a
            N_1 = ln_x * ln_n1
            ln_n2 = 1
            N_2 = ln_n2 * ln_x
            ln_n3 = ln_l1
            N_3 = ln_y * ln_n3
            ln_n5 = ln_l3
            N_5 = ln_v * ln_n5
            ln_n6 = (1 - ln_w * tan_a)
            N_6 = ln_n6 * ln_v
            N_4 = ln_n4y * ln_y
            N_total = Eq(N_1 + N_2 + N_3 + N_4 + N_5 + N_6, area_each_shape)
            res_N = solve(N_total, ln_n4y)
            print("to solve n4_y: ", res_N[0])
            ln_n4 = res_N[0]

            # J-Part
            ln_j1 = ln_y * tan_a
            J_1 = ln_y * ln_j1
            ln_j2 = ln_v * tan_a
            J_2 = ln_v * ln_j2
            ln_j4 = ln_w * tan_a
            J_4 = ln_w * ln_j4
            ln_j5 = 1 - ln_j4
            J_5 = ln_j5 * ln_w
            J_3 = ln_j3y * ln_v
            J_total = Eq(J_1 + J_2 + J_3 + J_4 + J_5, area_each_shape)
            res_J = solve(J_total, ln_j3y)
            print("to solve j3_y: ", res_J[0])
            ln_j3 = res_J[0]

            print("check A: ", area_each_shape, " --> 3x")
            print("check L: ", L_1 + ln_l2 * ln_y + L_3 + L_4 + L_5)
            print("check N: ", N_1 + N_2 + N_3 + ln_n4 * ln_y + N_5 + N_6)
            print("check J: ", J_1 + J_2 + ln_j3 * ln_v + J_4 + J_5)

            return ln_l1, ln_l2, ln_l3, ln_l4, ln_l5, \
                   ln_n1, ln_n2, ln_n3, ln_n4, ln_n5, ln_n6, \
                   ln_j1, ln_j2, ln_j3, ln_j4, ln_j5

        ln_l1, ln_l2, ln_l3, ln_l4, ln_l5,\
        ln_n1, ln_n2, ln_n3, ln_n4, ln_n5, ln_n6,\
        ln_j1, ln_j2, ln_j3, ln_j4, ln_j5\
            = shape_calculator()

        # scaled..
        print("check scale (x,y): ", x_scale, y_scale)
        print("--> scale factor (1): ", hex_width)
        print("radius : ", radius)


        x_t = ln_x * radius
        print("x: ", ln_x)
        print("x_t :", x_t)
        y_t = hex_width - x_t
        v_t = ln_v * radius
        print("v: ", ln_v)
        print("v_t :", v_t)
        w_t = hex_width - v_t
        l1_t = ln_l1 * radius
        l2_t = ln_l2 * radius
        print("scaled l2_t: ", l2_t)
        n4_t = ln_n4 * radius
        n6_t = ln_n6 * radius
        j3_t = ln_j3 * radius

        def positioning(x_max, y_max, x_position, y_position):
            x_offset = 0
            if x_position == 1:  # left (default)
                x_offset = 0
            if x_position == 2:  # center
                x_offset = x_max
            if x_position == 3:  # right
                x_offset = 2 * x_max
            y_offset = 0
            if y_position == 8:  # up (default)
                y_offset = 0
            if y_position == 5:  # center
                y_offset = y_max
            if y_position == 2:  # down
                y_offset = 2 * y_max

            return x_offset, y_offset

        def set_hexagon(ctx, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            print("print hexagon mit offset: ", x_offset)
            ctx.move_to(x_max / 2 + x_offset, y_max + y_offset)
            ctx.line_to((x_max / 2 + x_offset) - (x_max / 2 * cos_a), y_max * 0.75 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) - (x_max / 2 * cos_a), y_max * 0.25 + y_offset)
            ctx.line_to(x_max / 2 + x_offset, 0 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) + (x_max / 2 * cos_a), y_max * 0.25 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) + (x_max / 2 * cos_a), y_max * 0.75 + y_offset)
            ctx.close_path()
            ctx.set_source_rgb(0, 0, 1)
            ctx.set_line_width(1.2)
            ctx.stroke()

        def set_circle(ctx, x_0, y_0, rad_0, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            ctx.arc(x_0 + x_offset, y_0 + y_offset, rad_0, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 0, 0)
            ctx.set_line_width(1)
            ctx.stroke()

        def set_point(ctx, name, x_pos, y_pos, align, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            ctx.set_font_size(10)
            ctx.select_font_face("Arial",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
            s = str(name)
            xbearing, ybearing, width, height, dx, dy = ctx.text_extents(s)
            x_pos, y_pos = x_pos + x_offset, y_pos + y_offset
            # default (9): text is left-justified/above
            x_0, y_0 = x_pos, y_pos
            set_circle(ctx, x_0, y_0, 2, 1, 0, 0, 0)
            if align == 7:
                # (7): right-justified/above
                x_0, y_0 = x_pos - dx, y_pos
            if align == 3:
                # (3): right-justified/under
                x_0, y_0 = x_pos - dx, y_pos - ybearing
            if align == 5:
                # (5): centered
                x_0, y_0 = x_pos - dx / 2, y_pos - ybearing / 2
            if align == 1:
                # (1): left-justified/under
                x_0, y_0 = x_pos, y_pos - ybearing
            ctx.move_to(x_0, y_0)
            ctx.set_source_rgba(0, 0, 0, 1)
            ctx.show_text(s)
            ctx.stroke()

        def set_polygon_L(ctx, x_0, y_0, x_position, y_position):

            # lines
            ctx.move_to(x_0, y_0)
            L_x1, L_y1 = x_0 - y_t, y_0 - y_t * tan_a
            ctx.line_to(L_x1, L_y1)
            L_x2, L_y2 = L_x1,  L_y1 - l2_t - y_t * tan_a   # L_y1 - y_t / cos_a
            # print("check l1_t ", y_t*tan_a)
            ctx.line_to(L_x2, L_y2)
            L_x3, L_y3 = x_0, y_0 - l2_t - y_t * tan_a   # y_t / cos_a
            ctx.line_to(L_x3, L_y3)
            L_x4, L_y4 = x_0 + v_t, L_y3 - v_t * sin_a
            ctx.line_to(L_x4, L_y4)
            L_x5, L_y5 = x_0 + hex_width, y_0 * 0.75
            ctx.line_to(L_x5, L_y5)
            ctx.close_path()

            # color
            clr_L = cairo.RadialGradient(x_scale / 2, y_0 / 2, 5, x_scale / 2, y_0 / 2, radius)
            clr_L.add_color_stop_rgba(0, 0, 0, 1, 1)
            clr_L.add_color_stop_rgba(1, 0, 1, 0, 1)
            ctx.set_source(clr_L)
            ctx.fill()

            return (L_x1, L_y1), (L_x2, L_y2), (L_x3, L_y3), (L_x4, L_y4), (L_x5, L_y5)

        def set_polygon_J(ctx, x_0, y_0, x_position, y_position):
            """todo"""

            # lines
            ctx.move_to(x_0, y_0)
            J_x1 = x_0 - y_t
            J_y1 = y_0 - y_t * tan_a

        def set_polygon_N(ctx, x_0, y_0, L_x1, L_y1, L_x2, L_y2, L_x3, L_y3, L_x4, L_y4, x_position, y_position):
            # lines
            ctx.move_to(x_0, y_0)
            ctx.line_to(L_x1, L_y1)
            ctx.line_to(L_x2, L_y2)
            ctx.line_to(L_x3, L_y3)
            ctx.line_to(L_x4, L_y4)
            N_x6, N_y6 = L_x4, L_y4 - n6_t
            ctx.line_to(N_x6, N_y6)
            N_x5, N_y5 = (x_scale / 2), N_y6 - v_t * sin_a
            ctx.line_to(N_x5, N_y5)
            N_x4, N_y4 = (x_scale / 2), y_scale - 2*y_t * tan_a - l2_t - n4_t
            ctx.line_to(N_x4, N_y4)
            # todo
            N_x3, N_y3 = L_x2, y_scale * 0.25 - x_t * tan_a
            ctx.line_to(N_x3, N_y3)

            N_x2, N_y2 = (x_scale / 2) - (x_scale / 2 * cos_a), y_scale * 0.25
            ctx.line_to(N_x2, N_y2)

            ctx.close_path()

            # color
            clr_L = cairo.RadialGradient(x_scale / 2, y_0 / 2, 5, x_scale / 2, y_0 / 2, radius)
            clr_L.add_color_stop_rgba(0, 0, 1, 0, 1)
            clr_L.add_color_stop_rgba(1, 1, 0, 0, 1)
            ctx.set_source(clr_L)
            ctx.fill()

        def set_helplines(ctx, x_0, y_0, x_line1, x_line2, x_position, y_position):
            """
            sets helplines: horizontal and vertical center, 4 vertical lines which defines the polygons
            :param ctx:
            :param x_0:
            :param y_0:
            :param x_line1:
            :param x_line2:
            :return:
            """
            x_offset = 0
            if x_position == 1:  # left
                x_offset = 0
            if x_position == 2:  # center
                x_offset = x_0
            if x_position == 3:  # right
                x_offset = 2 * x_0
            print("print helplines with offset: ", x_offset)

            # horizontal center
            ctx.move_to(0 + x_offset, y_0)
            H_x1, H_y1 = x_scale + x_offset, y_0
            ctx.line_to(H_x1, H_y1)
            # vertical center
            H_x2, H_y2 = x_center + x_offset, 0
            ctx.move_to(H_x2, H_y2)
            H_x3, H_y3 = x_center + x_offset, y_scale
            ctx.line_to(H_x3, H_y3)

            # vertical line1
            H_x4, H_y4 = x_center + x_offset - x_line1, 0
            ctx.move_to(H_x4, H_y4)
            H_x5, H_y5 = x_center + x_offset - x_line1, y_scale
            ctx.line_to(H_x5, H_y5)
            # vertical line2
            H_x6, H_y6 = x_center + x_offset + x_line2, 0
            ctx.move_to(H_x6, H_y6)
            H_x7, H_y7 = x_center + x_offset + x_line2, y_scale
            ctx.line_to(H_x7, H_y7)
            # vertical frame left
            H_x8, H_y8 = x_center + x_offset - hex_width, 0
            ctx.move_to(H_x8, H_y8)
            H_x9, H_y9 = x_center + x_offset - hex_width, y_scale
            ctx.line_to(H_x9, H_y9)
            # vertical frame right
            H_x10, H_y10 = x_center + x_offset + hex_width, 0
            ctx.move_to(H_x10, H_y10)
            H_x11, H_y11 = x_center + x_offset + hex_width, y_scale
            ctx.line_to(H_x11, H_y11)

            # corner to center
            M_x, M_y = x_center + x_offset, y_center
            N1_x, N1_y = (x_scale / 2) - (x_scale / 2 * cos_a) + x_offset, y_scale * 0.75
            N2_x, N2_y = (x_scale / 2) - (x_scale / 2 * cos_a) + x_offset, y_scale * 0.25
            J1_x, J1_y = x_center + x_offset, 0
            J2_x, J2_y = (x_scale / 2) + (x_scale / 2 * cos_a) + x_offset, y_scale * 0.25
            L5_x, L5_y = (x_scale / 2) + (x_scale / 2 * cos_a) + x_offset, y_scale * 0.75
            L0_x, L0_y = x_center + x_offset, y_scale
            ctx.move_to(M_x, M_y)
            ctx.line_to(N1_x, N1_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(N2_x, N2_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(J1_x, J1_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(J2_x, J2_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(L5_x, L5_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(L0_x, L0_y)



            # color
            ctx.set_source_rgb(1, 0, 0)
            ctx.set_line_width(0.5)
            ctx.stroke()

            return H_x1, H_x2, H_x3, H_x4, H_x5, H_x6, H_x7, H_x8, H_x8, H_x9, H_x10, H_x11, \
                   H_y1, H_y2, H_y3, H_y4, H_y5, H_y6, H_y7, H_y8, H_y9, H_y10, H_y11

        """
        *** program / process ***
        """
        with cairo.SVGSurface("NJL_Logo.svg", 3 * x_scale, 3 * y_scale) as surface:
            context = cairo.Context(surface)

            # hexagon --> upper line
            set_hexagon(context, x_scale, y_scale, 1, 0)
            set_hexagon(context, x_scale, y_scale, 2, 0)
            set_hexagon(context, x_scale, y_scale, 3, 0)
            """# --> center line
            set_hexagon(context, x_scale, y_scale, 1, 5)
            set_hexagon(context, x_scale, y_scale, 2, 5)
            set_hexagon(context, x_scale, y_scale, 3, 5)

            # --> under line
            set_hexagon(context, x_scale, y_scale, 1, 2)
            set_hexagon(context, x_scale, y_scale, 2, 2)
            set_hexagon(context, x_scale, y_scale, 3, 2)
            """
            # circle --> upper line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 0)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 0)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 0)
            """# --> center line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 5)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 5)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 5)

            # --> under line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 2)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 2)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 2)
            """
            # set polygon L
            L_x0 = x_center
            L_y0 = y_scale
            (L_x1, L_y1), (L_x2, L_y2), (L_x3, L_y3), (L_x4, L_y4), (L_x5, L_y5) =\
                set_polygon_L(context, L_x0, L_y0, 0, 0)

            # todo:set polygon J

            # todo:set polygon N
            N_x0 = (x_scale / 2) - (x_scale / 2 * cos_a)
            N_y0 = y_scale * 0.75
            set_polygon_N(context, N_x0, N_y0, L_x1, L_y1, L_x2, L_y2,
                          L_x3, L_y3, L_x4, L_y4, 0, 0)

            # helplines
            h_x1, h_x2, h_x3, h_x4, h_x5, h_x6, h_x7, h_x8, h_x8, h_x9, h_x10, h_x11, h_y1, h_y2, h_y3, h_y4, h_y5, h_y6, \
            h_y7, h_y8, h_y9, h_y10, h_y11 = set_helplines(context, x_scale, y_center, y_t, v_t, 1, 0)
            set_helplines(context, x_scale, y_center, y_t, v_t, 2, 0)
            set_helplines(context, x_scale, y_center, y_t, v_t, 3, 0)

            # set points
            set_point(context, "L0:(" + str(x_center) + "|" + str(y_scale) + ")"
                      , x_center, y_scale, 7, x_scale, y_scale, 1, 0)
            set_point(context, "L1:(" + str(round(L_x1, 1)) + "|" + str(round(L_y1, 1)) + ")"
                      , L_x1, L_y1, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L2:(" + str(round(L_x2, 1)) + "|" + str(round(L_y2, 1)) + ")"
                      , L_x2, L_y2, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L3:(" + str(round(L_x3, 1)) + "|" + str(round(L_y3, 1)) + ")"
                      , L_x3, L_y3, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L4:(" + str(round(L_x4, 1)) + "|" + str(round(L_y4, 1)) + ")"
                      , L_x4, L_y4, 3, x_scale, y_scale, 1, 0)
            set_point(context, "L5:(" + str(round(L_x5, 1)) + "|" + str(round(L_y5, 1)) + ")"
                      , L_x5, L_y5, 7, x_scale, y_scale, 1, 0)

            set_point(context, "H0:(" + str(round(0, 1)) + "|" + str(round(y_center, 1)) + ")"
                      , 0, y_center, 9, x_scale, y_scale, 1, 0)
            set_point(context, "H1:(" + str(round(h_x1, 1)) + "|" + str(round(h_y1, 1)) + ")"
                      , h_x1, h_y1, 7, x_scale, y_scale, 1, 0)
            set_point(context, "H2:(" + str(round(h_x2, 1)) + "|" + str(round(h_y2, 1)) + ")"
                      , h_x2, h_y2, 1, x_scale, y_scale, 1, 0)

        # printing message when file is saved
        print("File Saved")


LogoConstructor().draw_logo(300)


class NJLLogoConstructor:
    """
    31.08.2023
    """
    angle_alpha = 30
    sin_a = abs(math.sin(math.radians(angle_alpha)))
    cos_a = abs(math.cos(math.radians(angle_alpha)))
    tan_a = abs(math.tan(math.radians(angle_alpha)))

    def draw_logo(self, radius):
        # trigonometry
        sin_a = self.sin_a
        cos_a = self.cos_a
        tan_a = self.tan_a

        # dimensions:
        x_scale = y_scale = radius * 2
        x_center = y_center = radius
        hex_width = radius * cos_a
        # hexagon, area:
        area_hexagon = 6 * math.pow(1, 2) * math.sqrt(3) / 4
        area_each_shape = area_hexagon / 3

        # vars:
        ln_x, ln_v, ln_n6 = symbols('x v n6', real=True)

        # calc  the lines
        def shape_calculator():
            """
            31.08.2023
            :return: all vertical lines from the L-, J- and N-shapes
            """
            # vars:
            ln_y = cos_a - ln_x
            ln_w = cos_a - ln_v

            # L-Part
            L_12 = (1 - ln_v) * ln_y
            L_34 = (1 - ln_v) * ln_v
            L_5 = 0.5 * (1 - ln_v) * ln_w

            # N-Part
            N_1 = ln_x * (ln_x * tan_a)
            N_2 = 1 * ln_x
            N_3 = ln_y * (ln_y * tan_a)
            N_4 = ((1 + ln_x * tan_a) - (ln_y * tan_a) - (1 - ln_v)) * ln_y
            N_5 = ln_v * (ln_v * tan_a)
            N_6 = ln_n6 * ln_v

            # J-Part
            J_1 = ln_y * (ln_y * tan_a)
            J_23 = (1 - ln_n6) * ln_v
            J_4 = ln_w * (ln_w * tan_a)
            J_5 = (1 - (ln_w * tan_a)) * ln_w

            equations = [
                Eq(L_12 + L_34 + L_5, area_each_shape),
                Eq(N_1 + N_2 + N_3 + N_4 + N_5 + N_6, area_each_shape),
                Eq(J_1 + J_23 + J_4 + J_5, area_each_shape),
                ]

            result_equations = solve(equations)
            print("result: ", result_equations)
            dummy = 0

            return dummy

        fb_res = shape_calculator()

        # scaled..
        print("check scale (x,y): ", x_scale, y_scale)
        print("--> scale factor (1): ", hex_width)
        print("radius : ", radius)

        x_t = ln_x * radius
        print("x: ", ln_x)
        print("x_t :", x_t)
        y_t = hex_width - x_t
        v_t = ln_v * radius
        print("v: ", ln_v)
        print("v_t :", v_t)
        w_t = hex_width - v_t
        l1_t = 1# ln_l1 * radius
        l2_t = 1# ln_l2 * radius
        print("scaled l2_t: ", l2_t)
        n4_t = 1# ln_n4 * radius
        n6_t = 1# ln_n6 * radius
        j3_t = 1# ln_j3 * radius




        def positioning(x_max, y_max, x_position, y_position):
            x_offset = 0
            if x_position == 1:  # left (default)
                x_offset = 0
            if x_position == 2:  # center
                x_offset = x_max
            if x_position == 3:  # right
                x_offset = 2 * x_max
            y_offset = 0
            if y_position == 8:  # up (default)
                y_offset = 0
            if y_position == 5:  # center
                y_offset = y_max
            if y_position == 2:  # down
                y_offset = 2 * y_max

            return x_offset, y_offset

        def set_hexagon(ctx, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            print("print hexagon mit offset: ", x_offset)
            ctx.move_to(x_max / 2 + x_offset, y_max + y_offset)
            ctx.line_to((x_max / 2 + x_offset) - (x_max / 2 * cos_a), y_max * 0.75 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) - (x_max / 2 * cos_a), y_max * 0.25 + y_offset)
            ctx.line_to(x_max / 2 + x_offset, 0 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) + (x_max / 2 * cos_a), y_max * 0.25 + y_offset)
            ctx.line_to((x_max / 2 + x_offset) + (x_max / 2 * cos_a), y_max * 0.75 + y_offset)
            ctx.close_path()
            ctx.set_source_rgb(0, 0, 1)
            ctx.set_line_width(1.2)
            ctx.stroke()

        def set_circle(ctx, x_0, y_0, rad_0, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            ctx.arc(x_0 + x_offset, y_0 + y_offset, rad_0, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 0, 0)
            ctx.set_line_width(1)
            ctx.stroke()

        def set_point(ctx, name, x_pos, y_pos, align, x_max, y_max, x_position, y_position):
            x_offset, y_offset = positioning(x_max, y_max, x_position, y_position)

            ctx.set_font_size(10)
            ctx.select_font_face("Arial",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
            s = str(name)
            xbearing, ybearing, width, height, dx, dy = ctx.text_extents(s)
            x_pos, y_pos = x_pos + x_offset, y_pos + y_offset
            # default (9): text is left-justified/above
            x_0, y_0 = x_pos, y_pos
            set_circle(ctx, x_0, y_0, 2, 1, 0, 0, 0)
            if align == 7:
                # (7): right-justified/above
                x_0, y_0 = x_pos - dx, y_pos
            if align == 3:
                # (3): right-justified/under
                x_0, y_0 = x_pos - dx, y_pos - ybearing
            if align == 5:
                # (5): centered
                x_0, y_0 = x_pos - dx / 2, y_pos - ybearing / 2
            if align == 1:
                # (1): left-justified/under
                x_0, y_0 = x_pos, y_pos - ybearing
            ctx.move_to(x_0, y_0)
            ctx.set_source_rgba(0, 0, 0, 1)
            ctx.show_text(s)
            ctx.stroke()

        def set_polygon_L(ctx, x_0, y_0, x_position, y_position):

            # lines
            ctx.move_to(x_0, y_0)
            L_x1, L_y1 = x_0 - y_t, y_0 - y_t * tan_a
            ctx.line_to(L_x1, L_y1)
            L_x2, L_y2 = L_x1,  L_y1 - l2_t - y_t * tan_a   # L_y1 - y_t / cos_a
            # print("check l1_t ", y_t*tan_a)
            ctx.line_to(L_x2, L_y2)
            L_x3, L_y3 = x_0, y_0 - l2_t - y_t * tan_a   # y_t / cos_a
            ctx.line_to(L_x3, L_y3)
            L_x4, L_y4 = x_0 + v_t, L_y3 - v_t * sin_a
            ctx.line_to(L_x4, L_y4)
            L_x5, L_y5 = x_0 + hex_width, y_0 * 0.75
            ctx.line_to(L_x5, L_y5)
            ctx.close_path()

            # color
            clr_L = cairo.RadialGradient(x_scale / 2, y_0 / 2, 5, x_scale / 2, y_0 / 2, radius)
            clr_L.add_color_stop_rgba(0, 0, 0, 1, 1)
            clr_L.add_color_stop_rgba(1, 0, 1, 0, 1)
            ctx.set_source(clr_L)
            ctx.fill()

            return (L_x1, L_y1), (L_x2, L_y2), (L_x3, L_y3), (L_x4, L_y4), (L_x5, L_y5)

        def set_polygon_J(ctx, x_0, y_0, x_position, y_position):
            """todo"""

            # lines
            ctx.move_to(x_0, y_0)
            J_x1 = x_0 - y_t
            J_y1 = y_0 - y_t * tan_a

        def set_polygon_N(ctx, x_0, y_0, L_x1, L_y1, L_x2, L_y2, L_x3, L_y3, L_x4, L_y4, x_position, y_position):
            # lines
            ctx.move_to(x_0, y_0)
            ctx.line_to(L_x1, L_y1)
            ctx.line_to(L_x2, L_y2)
            ctx.line_to(L_x3, L_y3)
            ctx.line_to(L_x4, L_y4)
            N_x6, N_y6 = L_x4, L_y4 - n6_t
            ctx.line_to(N_x6, N_y6)
            N_x5, N_y5 = (x_scale / 2), N_y6 - v_t * sin_a
            ctx.line_to(N_x5, N_y5)
            N_x4, N_y4 = (x_scale / 2), y_scale - 2*y_t * tan_a - l2_t - n4_t
            ctx.line_to(N_x4, N_y4)
            # todo
            N_x3, N_y3 = L_x2, y_scale * 0.25 - x_t * tan_a
            ctx.line_to(N_x3, N_y3)

            N_x2, N_y2 = (x_scale / 2) - (x_scale / 2 * cos_a), y_scale * 0.25
            ctx.line_to(N_x2, N_y2)

            ctx.close_path()

            # color
            clr_L = cairo.RadialGradient(x_scale / 2, y_0 / 2, 5, x_scale / 2, y_0 / 2, radius)
            clr_L.add_color_stop_rgba(0, 0, 1, 0, 1)
            clr_L.add_color_stop_rgba(1, 1, 0, 0, 1)
            ctx.set_source(clr_L)
            ctx.fill()

        def set_helplines(ctx, x_0, y_0, x_line1, x_line2, x_position, y_position):
            """
            sets helplines: horizontal and vertical center, 4 vertical lines which defines the polygons
            :param ctx:
            :param x_0:
            :param y_0:
            :param x_line1:
            :param x_line2:
            :return:
            """
            x_offset = 0
            if x_position == 1:  # left
                x_offset = 0
            if x_position == 2:  # center
                x_offset = x_0
            if x_position == 3:  # right
                x_offset = 2 * x_0
            print("print helplines with offset: ", x_offset)

            # horizontal center
            ctx.move_to(0 + x_offset, y_0)
            H_x1, H_y1 = x_scale + x_offset, y_0
            ctx.line_to(H_x1, H_y1)
            # vertical center
            H_x2, H_y2 = x_center + x_offset, 0
            ctx.move_to(H_x2, H_y2)
            H_x3, H_y3 = x_center + x_offset, y_scale
            ctx.line_to(H_x3, H_y3)

            # vertical line1
            H_x4, H_y4 = x_center + x_offset - x_line1, 0
            ctx.move_to(H_x4, H_y4)
            H_x5, H_y5 = x_center + x_offset - x_line1, y_scale
            ctx.line_to(H_x5, H_y5)
            # vertical line2
            H_x6, H_y6 = x_center + x_offset + x_line2, 0
            ctx.move_to(H_x6, H_y6)
            H_x7, H_y7 = x_center + x_offset + x_line2, y_scale
            ctx.line_to(H_x7, H_y7)
            # vertical frame left
            H_x8, H_y8 = x_center + x_offset - hex_width, 0
            ctx.move_to(H_x8, H_y8)
            H_x9, H_y9 = x_center + x_offset - hex_width, y_scale
            ctx.line_to(H_x9, H_y9)
            # vertical frame right
            H_x10, H_y10 = x_center + x_offset + hex_width, 0
            ctx.move_to(H_x10, H_y10)
            H_x11, H_y11 = x_center + x_offset + hex_width, y_scale
            ctx.line_to(H_x11, H_y11)

            # corner to center
            M_x, M_y = x_center + x_offset, y_center
            N1_x, N1_y = (x_scale / 2) - (x_scale / 2 * cos_a) + x_offset, y_scale * 0.75
            N2_x, N2_y = (x_scale / 2) - (x_scale / 2 * cos_a) + x_offset, y_scale * 0.25
            J1_x, J1_y = x_center + x_offset, 0
            J2_x, J2_y = (x_scale / 2) + (x_scale / 2 * cos_a) + x_offset, y_scale * 0.25
            L5_x, L5_y = (x_scale / 2) + (x_scale / 2 * cos_a) + x_offset, y_scale * 0.75
            L0_x, L0_y = x_center + x_offset, y_scale
            ctx.move_to(M_x, M_y)
            ctx.line_to(N1_x, N1_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(N2_x, N2_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(J1_x, J1_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(J2_x, J2_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(L5_x, L5_y)
            ctx.move_to(M_x, M_y)
            ctx.line_to(L0_x, L0_y)



            # color
            ctx.set_source_rgb(1, 0, 0)
            ctx.set_line_width(0.5)
            ctx.stroke()

            return H_x1, H_x2, H_x3, H_x4, H_x5, H_x6, H_x7, H_x8, H_x8, H_x9, H_x10, H_x11, \
                   H_y1, H_y2, H_y3, H_y4, H_y5, H_y6, H_y7, H_y8, H_y9, H_y10, H_y11


        """
        *** program / process ***
        """
        with cairo.SVGSurface("NJL_Logo.svg", 3 * x_scale, 3 * y_scale) as surface:
            context = cairo.Context(surface)

            # hexagon --> upper line
            set_hexagon(context, x_scale, y_scale, 1, 0)
            set_hexagon(context, x_scale, y_scale, 2, 0)
            set_hexagon(context, x_scale, y_scale, 3, 0)
            """# --> center line
            set_hexagon(context, x_scale, y_scale, 1, 5)
            set_hexagon(context, x_scale, y_scale, 2, 5)
            set_hexagon(context, x_scale, y_scale, 3, 5)

            # --> under line
            set_hexagon(context, x_scale, y_scale, 1, 2)
            set_hexagon(context, x_scale, y_scale, 2, 2)
            set_hexagon(context, x_scale, y_scale, 3, 2)
            """
            # circle --> upper line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 0)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 0)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 0)
            """# --> center line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 5)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 5)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 5)

            # --> under line
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 1, 2)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 2, 2)
            set_circle(context, x_scale / 2, y_scale / 2, radius, x_scale, y_scale, 3, 2)
            """
            # set polygon L
            L_x0 = x_center
            L_y0 = y_scale
            (L_x1, L_y1), (L_x2, L_y2), (L_x3, L_y3), (L_x4, L_y4), (L_x5, L_y5) =\
                set_polygon_L(context, L_x0, L_y0, 0, 0)

            # todo:set polygon J

            # todo:set polygon N
            N_x0 = (x_scale / 2) - (x_scale / 2 * cos_a)
            N_y0 = y_scale * 0.75
            set_polygon_N(context, N_x0, N_y0, L_x1, L_y1, L_x2, L_y2,
                          L_x3, L_y3, L_x4, L_y4, 0, 0)

            # helplines
            h_x1, h_x2, h_x3, h_x4, h_x5, h_x6, h_x7, h_x8, h_x8, h_x9, h_x10, h_x11, h_y1, h_y2, h_y3, h_y4, h_y5, h_y6, \
            h_y7, h_y8, h_y9, h_y10, h_y11 = set_helplines(context, x_scale, y_center, y_t, v_t, 1, 0)
            set_helplines(context, x_scale, y_center, y_t, v_t, 2, 0)
            set_helplines(context, x_scale, y_center, y_t, v_t, 3, 0)

            # set points
            set_point(context, "L0:(" + str(x_center) + "|" + str(y_scale) + ")"
                      , x_center, y_scale, 7, x_scale, y_scale, 1, 0)
            set_point(context, "L1:(" + str(round(L_x1, 1)) + "|" + str(round(L_y1, 1)) + ")"
                      , L_x1, L_y1, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L2:(" + str(round(L_x2, 1)) + "|" + str(round(L_y2, 1)) + ")"
                      , L_x2, L_y2, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L3:(" + str(round(L_x3, 1)) + "|" + str(round(L_y3, 1)) + ")"
                      , L_x3, L_y3, 9, x_scale, y_scale, 1, 0)
            set_point(context, "L4:(" + str(round(L_x4, 1)) + "|" + str(round(L_y4, 1)) + ")"
                      , L_x4, L_y4, 3, x_scale, y_scale, 1, 0)
            set_point(context, "L5:(" + str(round(L_x5, 1)) + "|" + str(round(L_y5, 1)) + ")"
                      , L_x5, L_y5, 7, x_scale, y_scale, 1, 0)

            set_point(context, "H0:(" + str(round(0, 1)) + "|" + str(round(y_center, 1)) + ")"
                      , 0, y_center, 9, x_scale, y_scale, 1, 0)
            set_point(context, "H1:(" + str(round(h_x1, 1)) + "|" + str(round(h_y1, 1)) + ")"
                      , h_x1, h_y1, 7, x_scale, y_scale, 1, 0)
            set_point(context, "H2:(" + str(round(h_x2, 1)) + "|" + str(round(h_y2, 1)) + ")"
                      , h_x2, h_y2, 1, x_scale, y_scale, 1, 0)

        # printing message when file is saved
        print("File Saved")


NJLLogoConstructor().draw_logo(300)

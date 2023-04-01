from fathom import Point, ORIGIN, centroid
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners
import fathom.layout as layout
import fathom.geometry as geo

def draw_nodes(canvas):
    r = layout.matrix(h_sep = 2.4, v_sep = 1.8, n_rows = 2, n_cols = 3, top_left = ORIGIN)
    selected = [r[1][0]] + r[0] + [r[1][2]]
    res = []
    for i, p in enumerate(selected):
        canvas.new_text(text=str(i), anchor=p)
        c = canvas.new_circle(center=p, radius=0.3)
        res.append(c)
    return res

if __name__ == '__main__':
    canvas = tikz.Canvas()

    nodes = draw_nodes(canvas)

    y1 = canvas.new_arrow(src=nodes[1], dst=nodes[0]).get_skeleton()
    canvas.new_text(text='\\small $y_1$', anchor=centroid(y1.vertices()), location=locations.EAST)

    y2 = canvas.new_arrow(src=nodes[2], dst=nodes[1]).get_skeleton()
    canvas.new_text(text='\\small $y_2$', anchor=centroid(y2.vertices()), location=locations.NORTH)

    y3 = canvas.new_arrow(src=nodes[3], dst=nodes[2]).get_skeleton()
    canvas.new_text(text='\\small $y_3$', anchor=centroid(y3.vertices()), location=locations.NORTH)

    y4 = canvas.new_arrow(src=nodes[4], dst=nodes[3]).get_skeleton()
    canvas.new_text(text='\\small $y_4$', anchor=centroid(y4.vertices()), location=locations.EAST)

    x1 = canvas.new_arrow(src=nodes[1], dst=nodes[4]).get_skeleton()
    canvas.new_text(text='\\small $x_1$', anchor=centroid(x1.vertices()), location=locations.NORTH)

    x2 = canvas.new_arrow(src=nodes[0], dst=nodes[4]).get_skeleton()
    canvas.new_text(text='\\small $x_2$', anchor=centroid(x2.vertices()), location=locations.NORTH)

    x3 = canvas.new_arrow(src=nodes[2], dst=nodes[4]).get_skeleton()
    canvas.new_text(text='\\small $x_3$', anchor=centroid(x3.vertices()), location=locations.EAST)

    x5 = canvas.new_arrow(src=nodes[0], dst=nodes[2]).get_skeleton()
    canvas.new_text(text='\\small $x_5$', anchor=centroid(x5.vertices()), location=locations.SOUTH)

    # x4
    start_pt = nodes[0].get_skeleton().center()
    stop_pt = nodes[1].get_skeleton().center()
    x_offset = Point(-0.3, 0)
    y_offset = Point(0, (stop_pt - start_pt).y * 0.3)
    seg = [
        canvas.new_line(src=nodes[0], dst=start_pt + x_offset + y_offset),
        canvas.new_line(src=start_pt + x_offset + y_offset, dst=stop_pt + x_offset - y_offset),
        canvas.new_arrow(src=stop_pt + x_offset - y_offset, dst=nodes[1]),
    ]
    canvas.new_text(text='\\small $x_4$', anchor=centroid(seg[1].get_skeleton().vertices()), location=locations.WEST)

    texts = ['5', '7', '-2', '-4', '-6']
    locs = [locations.SOUTH, locations.NORTH, locations.NORTH, locations.NORTH, locations.SOUTH]
    for n, text, loc in zip(nodes, texts, locs):
        pt = n.get_skeleton().center().copy()
        assert loc in (locations.NORTH, locations.SOUTH, )
        if loc == locations.NORTH:
            pt += Point(0, 0.3)
        else:
            pt -= Point(0, 0.3)
        canvas.new_text(text=text, anchor=pt, location=loc)

    print(canvas.draw())

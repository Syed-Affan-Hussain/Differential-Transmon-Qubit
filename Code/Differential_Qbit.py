#Research Paper : John M. Martinis "Surface loss calculations and design of a superconducting transmon qubit with tapered wiring"
#Code Author: Syed Affan Hussain
import numpy as np
import qiskit_metal as metal
from qiskit_metal import draw, Dict, designs
from qiskit_metal.qlibrary.core import QComponent
import math

class DifferentialTransmonWithCPW(QComponent):
    default_options = Dict(
        pad_width='100um',
        pad_length='1300um',
        pad_separation='60um',
        jj_length='0.1um',
        inductor_width='0.1um',
        taper_width='9.9um',
        cpw_width='12.5um',
        cpw_gap='7.5um',
        cpw_length='200um',
        ground_margin='50um',
        layer='1',
        layer_ground='1',
        hfss_inductance='15nH',
        hfss_capacitance='100fF',
        pos_x='0um',
        pos_y='0um',
        orientation='0'
    )

    def make(self):
        p = self.parse_options()
        pad_center_offset = (p.pad_separation + p.pad_width) / 2
        pad_inner_edge = p.pad_separation / 2
        cpw_y_offset = pad_center_offset + p.pad_width/2 + p.cpw_length/2

        pad_top = draw.rectangle(p.pad_length, p.pad_width, 0, pad_center_offset)
        pad_bottom = draw.rectangle(p.pad_length, p.pad_width, 0, -pad_center_offset)

        taper_top = draw.Polygon([
             (-p.jj_length/2, p.inductor_width/2 - 0.01e-6),
             (p.jj_length/2, p.inductor_width/2 - 0.01e-6),
             (p.taper_width/2, pad_inner_edge),
             (-p.taper_width/2, pad_inner_edge)
        ])
        taper_bottom = draw.Polygon([
            (-p.jj_length/2, -p.inductor_width/2 + 0.01e-6),
            (p.jj_length/2, -p.inductor_width/2 + 0.01e-6),
            (p.taper_width/2, -pad_inner_edge),
            (-p.taper_width/2, -pad_inner_edge)
        ])

        pad_top_merged = draw.union(pad_top, taper_top)
        pad_bottom_merged = draw.union(pad_bottom, taper_bottom)

        cpw_top = draw.rectangle(p.cpw_width, p.cpw_length, 0, cpw_y_offset)
        cpw_bottom = draw.rectangle(p.cpw_width, p.cpw_length, 0, -cpw_y_offset)
        cpw_gap_width = p.cpw_width + 2 * p.cpw_gap
        cpw_gap_top = draw.rectangle(cpw_gap_width, p.cpw_length, 0, cpw_y_offset)
        cpw_gap_bottom = draw.rectangle(cpw_gap_width, p.cpw_length, 0, -cpw_y_offset)

        pocket_width = p.pad_length + 2 * p.ground_margin
        pocket_height = 2 * (pad_center_offset + p.pad_width/2) + 2 * p.ground_margin
        pocket = draw.rectangle(pocket_width, pocket_height)

        jj_line = draw.LineString([(-p.jj_length/2, 0), (p.jj_length/2, 0)])

        def apply_transform(geom):
            return draw.translate(
                draw.rotate(geom, p.orientation, origin=(0, 0)),
                p.pos_x, p.pos_y
            )

        structures = [
            pad_top_merged, pad_bottom_merged,
            cpw_top, cpw_bottom,
            cpw_gap_top, cpw_gap_bottom,
            pocket, jj_line
        ]
        transformed = [apply_transform(s) for s in structures]

        self.add_qgeometry('poly', {
            'top_pad': transformed[0],
            'bottom_pad': transformed[1],
            'cpw_top': transformed[2],
            'cpw_bottom': transformed[3]
        }, layer=p.layer)

        self.add_qgeometry('poly', {
            'ground_pocket': transformed[6],
            'cpw_gap_top': transformed[4],
            'cpw_gap_bottom': transformed[5]
        }, layer=p.layer_ground, subtract=True)

        self.add_qgeometry('junction', {'jj': transformed[7]},
            layer=p.layer,
            width=p.inductor_width,
            hfss_inductance=p.hfss_inductance,
            hfss_capacitance=p.hfss_capacitance)

        def transform_point(point):
            x, y = point
            theta = math.radians(p.orientation)
            return (
                x * math.cos(theta) - y * math.sin(theta) + p.pos_x,
                x * math.sin(theta) + y * math.cos(theta) + p.pos_y
            )

        pin_top_start = transform_point((0, cpw_y_offset + p.cpw_length/2))
        pin_top_end = transform_point((0, cpw_y_offset - p.cpw_length/2))
        self.add_pin('Vpos', np.array([pin_top_start, pin_top_end]),
            width=p.cpw_width, input_as_norm=False)

        pin_bottom_start = transform_point((0, -cpw_y_offset - p.cpw_length/2))
        pin_bottom_end = transform_point((0, -cpw_y_offset + p.cpw_length/2))
        self.add_pin('Vneg', np.array([pin_bottom_start, pin_bottom_end]),
            width=p.cpw_width, input_as_norm=False)

if __name__ == "__main__":
    design = designs.DesignPlanar(overwrite_enabled=True)
    design.metadata['design_name'] = 'Differential_Transmon_v2'
    design.chips.main.size.update({'size_x': '5mm', 'size_y': '5mm'})

    qubit_options = {
        'pos_x': '0mm',
        'pos_y': '0mm',
        'jj_length': '0.1um', 
        'inductor_width': '0.1um',
        'ground_margin': '150um',
        'cpw_gap': '7.5um'
    }

    DifferentialTransmonWithCPW(design, 'qubit', options=qubit_options)
    gui = metal.MetalGUI(design)
    gui.rebuild()
    gui.autoscale()

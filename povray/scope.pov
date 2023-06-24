global_settings { max_trace_level 256 }

camera {
    angle 20
    location < 0, 62.3, 4.5 >
    look_at < 0, 0, 4.5 >
}

light_source {
    < 0, -39, 6 >
    colour < 1, 1, 1 >
}

#declare basic_prism = prism {
    linear_sweep
    linear_spline
    -41, // sweep the following shape from here ...
    60, // ... up through here
    4, // the number of points making up the shape ...
    < 6, 4 >, < -6, 4 >, < 0, -6 >, < 6, 4 >
}

difference {
    object {
        basic_prism
    }
    object {
        basic_prism
        scale < 0.9, 2, 0.9 >
    }
    rotate < 0, scope_rotation, 0 >
    scale < scope_scale, 1, scope_scale >
    translate < 0, 0, 6 >
    texture {
        pigment {
           colour rgbf < 1, 1, 1, 0 >
        }
        finish {
           ambient 0
           diffuse 0
           reflection { 0.93 }
        }
        normal {
            bumps 0.0018
        }
    }
}

plane {
    < 0, 1, 0 >, -40
    texture {
        pigment {
            image_map { png "tmp/flat.png" }
            rotate < 90, 0, 0 >
            scale < flat_scale_x, 1, flat_scale_y >
        }
        translate < flat_scale_x / 2, 0, flat_scale_y / 1.5 >
        finish {
            ambient 1
            diffuse 0
        }
    }
}

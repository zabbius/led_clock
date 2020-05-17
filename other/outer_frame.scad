$fn=64;


inner_width = 134.5;
inner_height = 117;
inner_depth = 20.3;

wall = 1;

outer_width = inner_width + wall * 2;
outer_height = inner_height + wall * 2;
outer_depth = inner_depth + wall;
border = 1.5;

screen_height = 99;

lineout_cutoff_height = 12;
lineout_cutoff_inner_offset = 2.5;
lineout_cutoff_y_offset = 4;

difference()
{
    translate([0, 0, outer_depth / 2])
        cube([outer_width, outer_height, outer_depth], center = true);
    
    translate([0, 0, outer_depth / 2 + wall])
        cube([inner_width, inner_height, outer_depth], center = true);
    
    translate([0, (inner_height - screen_height) / 2 - border / 2, 0])
        cube([inner_width - border * 2, screen_height - border, outer_depth], center = true);
    
    translate([-outer_width / 2, -inner_height / 2 + lineout_cutoff_height / 2 + lineout_cutoff_inner_offset -0.5, wall + outer_depth /2 + lineout_cutoff_y_offset])
        cube([wall * 4, lineout_cutoff_height, outer_depth], center = true);

    translate([58, -50, -wall])
        linear_extrude(wall * 3)
            polygon([[-12, 0], [0, -7], [0, 7]]);
}


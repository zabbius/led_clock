$fn=50;

wall = 1;

led_stand_h = 7;

pcb_hole_d = 3;
pcb_stand_d = 5;
pcb_stand_h2 = 3;


led_module_block_width = 132;
led_module_height = 32;
led_module_hole_d = 3;
led_module_hole_inset_y = 6;
led_module_stand_x_offset = 37;
led_module_stand_y_offset = 10;

led_module_gap = 1.5;

inner_box_depth=20;
inner_box_additional_height=15;

inner_box_screen_angles_cutoff = 10;

orange_inner_width = 48;
orange_inner_height = 46;
    

module pcb_stand( h )
{
    cylinder(h=h, d=pcb_stand_d);
    cylinder(h=h + pcb_stand_h2, d=pcb_hole_d);
}

module led_module_stand()
{
    translate([-led_module_stand_x_offset, -led_module_stand_y_offset, 0])
        pcb_stand(led_stand_h);
    translate([led_module_stand_x_offset, -led_module_stand_y_offset, 0])
        pcb_stand(led_stand_h);
    translate([-led_module_stand_x_offset, led_module_stand_y_offset, 0])
        pcb_stand(led_stand_h);
    translate([led_module_stand_x_offset, led_module_stand_y_offset, 0])
        pcb_stand(led_stand_h);
}

module 3_led_modules_stands()
{
    led_module_stand();
    translate([0, -led_module_height - led_module_gap, 0])
        led_module_stand();
    translate([0, led_module_height + led_module_gap, 0])
        led_module_stand();
    
}

inner_width = led_module_block_width;
inner_height = led_module_height * 3 + led_module_gap * 2;

outer_width = inner_width + wall * 2;
outer_height = inner_height + wall * 2;

cutoff_width = inner_width - inner_box_screen_angles_cutoff * 2; 

module back_box()
{
        
    difference() {
        translate([-outer_width/2, -outer_height/2])
            cube([outer_width, outer_height, inner_box_depth]);
        
        translate([-inner_width/2, -inner_height/2, wall])
            cube([inner_width, inner_height, inner_box_depth]);
        
        translate([-cutoff_width / 2, -inner_height / 2 - wall * 2, wall])
            cube([cutoff_width , wall * 3, inner_box_depth]);
    }
    
    difference() {
        translate([-outer_width / 2, -outer_height / 2 - inner_box_additional_height - wall])
            cube([outer_width, inner_box_additional_height + wall, inner_box_depth]);

        translate([-inner_width / 2, -outer_height / 2 - inner_box_additional_height, wall])
            cube([inner_width, inner_box_additional_height, inner_box_depth]);

    }
}



3_led_modules_stands();

difference() {
    back_box();
    translate([0, -inner_box_additional_height -outer_height / 2 + orange_inner_height / 2 + 1, 0])
        cube([orange_inner_width, orange_inner_height, 20], center = true);
    translate([inner_width / 2, -outer_height / 2- inner_box_additional_height / 2, inner_box_depth / 2])
        rotate([0, 90, 0])
            cylinder(h = wall * 10, d = phones_hole_d, center = true);
}

hole_center_offset = 3;
hole_diameter = 3;

hole_box_width= hole_diameter + 3;

module hole_box()
{
    linear_extrude(wall)
    difference()
    {
        square([hole_box_width, hole_box_width], center = true);
        circle(d=hole_diameter);
    }
}
    
lower_bound = outer_height / 2 + inner_box_additional_height;

translate([-orange_inner_width/2 + hole_box_width / 2, -lower_bound + hole_box_width / 2 + 1, 0])
    hole_box();

translate([orange_inner_width/2 - hole_box_width / 2, -lower_bound + hole_box_width / 2 + 1, 0])
    hole_box();

translate([orange_inner_width/2 - hole_box_width / 2, -lower_bound +orange_inner_height - hole_box_width / 2 + 1, 0])
    hole_box();

translate([-orange_inner_width/2 + hole_box_width / 2, -lower_bound +orange_inner_height - hole_box_width / 2 + 1, 0])
    hole_box();

phones_hole_d = 8;


motor_outer_diameter = 37;
motor_outer_length = 69.5;

module zchxd_motor(){
	
	/*
	
	cylinder 4 + face => d=6mm, h=15mm
	cylinder 3 => d=12mm, h=6mm
	cylinder 2 + holes (d=3mm)=> d=37mm, h=27mm
	cylinder 1 => d=34.5mm, h=30mm
	cylinder 0 (encoder) => d=27mm, h=69.5-30-27
	
	Encoder is a solid cylinder in the model as to replicate the space it would take up in reality
	
	*/
	
	total_height = motor_outer_length; //mm
	cyl_enc_diam = 27; 
	cyl_1_height = 30; 
	cyl_1_diam = motor_outer_diameter-2.5;
	cyl_2_diam = motor_outer_diameter;
	cyl_2_height = 27; 
	cyl_3_height = 6; 
	cyl_3_diam = 12;
	cyl_enc_height = total_height-cyl_1_height-cyl_2_height; 
	cyl_shift = 7; //distance from center of shaft to center of world
	hole_shift = 16; //distance from center of holes to center of world
	hole_diameter = 3; //M3 holes on top x9
	frag = 200; //number of fragments
	
	rotate([0,0,90]){
	
	cylinder(h=cyl_enc_height, d=cyl_2_diam+0.4, $fn=frag); //encoder 
	
	translate([0,0,cyl_enc_height-0.001]){
		cylinder(h=cyl_1_height+0.001, d=cyl_2_diam+0.4, $fn=frag); //cyl 1
		translate([0,0,cyl_1_height-0.001]){ 
			cylinder(h=cyl_2_height+0.4, d=cyl_2_diam+0.4, $fn=frag); //cyl 2
			
			difference(){		
				translate([0,cyl_shift,cyl_2_height+1]){
					translate([0,0,-10+0.001])
						cylinder(h=cyl_3_height+10+0.001, d=cyl_3_diam+0.4, $fn=frag); //cyl 3
					difference(){
						translate([0,0,0.001])
							cylinder(h=cyl_3_height+14, d=cyl_3_diam/2, $fn=frag); //cyl 4
						translate([-5,-cyl_3_diam/2-6,6+0.001]){
							cube([10,10,cyl_3_height+24]);
							}
						}
					translate([0,-cyl_shift,-1]){
						difference(){
							cylinder(h=1-0.001, d=cyl_1_diam+2.5+0.4-0.001, $fn=frag); //outer cyl
							translate([0,0,-0.001])
								cylinder(h=1+0.001, d=27, $fn=frag); //negative inner cyl
							
							
							}
							
							difference(){
								for(angle = [0:30:360]){  //to generate all M3 holes
									rotate([0,0,angle]){
										translate([hole_shift,0,0]){
											cylinder(h=10, d=3.2+0.4, $fn=frag);
											}
										}
									} 
									for(angle = [30:60:330]){ //to remove 6 M3 holes
										rotate([0,0,angle]){
											translate([hole_shift,0,-0.001]){
												cylinder(h=12+0.001, d=3+0.8, $fn=frag);
												}
											}
										}		  
										
									
									
							}

						}
					translate([0,0,-1]){
						cylinder(h=1, d=cyl_3_diam+4+0.4, $fn=frag); //skirting cyl
					}
				}
			}
			
			
			
			
			}
	}
}
}

//zchxd_motor();

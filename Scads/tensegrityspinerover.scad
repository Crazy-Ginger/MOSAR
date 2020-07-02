include <./cubemodule.scad>;
spring_hook_diameter=7;
spring_wire_diameter=3;
drive_shaft_length=12;

module wheelFlat(wheel_diameter=200, wheel_width=30, hub_diameter=30, shaft_diameter=6, shaft_length=drive_shaft_length, tread_thickness=5, tread_pitch=10, web_thickness=WALL_THICKNESS*2)
{
	key_width=shaft_diameter*0.085;
	treads_per_wheel=ceil((PI*wheel_diameter/tread_pitch)/2);
	tread_angle_increment=360/treads_per_wheel;
	
	echo("rotate([0,0,90]) wheelFlat(",wheel_diameter, wheel_width, hub_diameter, shaft_diameter, shaft_length, tread_thickness, tread_pitch, web_thickness,");");
	
	difference()
	{
		//Wheel surface
		cylinder(d=wheel_diameter, h=wheel_width);
		
		//Web around hub
		difference()
		{
			translate([0,0,web_thickness+DELTA])
				cylinder(d=wheel_diameter-tread_thickness*2, h=wheel_width-web_thickness, $fn=treads_per_wheel);
			
			cylinder(d=hub_diameter, h=shaft_length, $fn=treads_per_wheel);
		}
		
		//Tread around surface
		for(tread_angle=[0:tread_angle_increment:360])
			rotate([0,0,tread_angle])
				translate([wheel_diameter/2-tread_thickness/2,-tread_pitch/2,-DELTA])
					cube([tread_thickness,tread_pitch,wheel_width+2*DELTA]);
		
		//Motor shaft
		difference()
		{
			translate([0,0,-DELTA])
				cylinder(d=shaft_diameter, h=wheel_width+3*DELTA, $fn=treads_per_wheel);
			
			//Key cut
			translate([shaft_diameter/2-key_width,-shaft_diameter/2,-DELTA])
				cube([shaft_diameter,shaft_diameter,wheel_width+5*DELTA]);
		}
	}
}

module coil(r1, r2, h, n)
{
	hr = h / (n * 2);
	stepsize = 1/4;
	module segment(i1, i2) {
		alpha1 = i1 * 360*r2/hr;
		alpha2 = i2 * 360*r2/hr;
		len1 = sin(acos(i1*2-1))*r2;
		len2 = sin(acos(i2*2-1))*r2;
		if (len1 < 0.01)
			polygon([
				[ cos(alpha1)*r1, sin(alpha1)*r1 ],
				[ cos(alpha2)*(r1-len2), sin(alpha2)*(r1-len2) ],
				[ cos(alpha2)*(r1+len2), sin(alpha2)*(r1+len2) ]
			]);
		if (len2 < 0.01)
			polygon([
				[ cos(alpha1)*(r1+len1), sin(alpha1)*(r1+len1) ],
				[ cos(alpha1)*(r1-len1), sin(alpha1)*(r1-len1) ],
				[ cos(alpha2)*r1, sin(alpha2)*r1 ],
			]);
		if (len1 >= 0.01 && len2 >= 0.01)
			polygon([
				[ cos(alpha1)*(r1+len1), sin(alpha1)*(r1+len1) ],
				[ cos(alpha1)*(r1-len1), sin(alpha1)*(r1-len1) ],
				[ cos(alpha2)*(r1-len2), sin(alpha2)*(r1-len2) ],
				[ cos(alpha2)*(r1+len2), sin(alpha2)*(r1+len2) ]
			]);
	}
	linear_extrude(height = h, twist = 180*h/hr,
			$fn = (hr/r2)/stepsize, convexity = 5) {
		for (i = [ stepsize : stepsize : 1+stepsize/2 ])
			segment(i-stepsize, min(i, 1));
	}
}

module hookToroid()
{
	rotate_extrude(convexity = 4)
		translate([spring_hook_diameter/2+spring_wire_diameter, 0, 0])
			circle(d = spring_hook_diameter);
}

module motorMountMicro(size=[10,12,28.5], encoderSize=[12,12,5], shaftDiameter=3, shaftLength=9, wallThickness=WALL_THICKNESS)
{
	mountsize=[size[0]+wallThickness*2,size[1]+wallThickness*2,size[2]];
	
	difference()
	{
		//remove wallThickness to cover top	vv
		translate([-mountsize[0]/2-wallThickness-DELTA,-mountsize[1]/2,-mountsize[2]+wallThickness])
			cube(mountsize, center=false);
		
		translate([-size[0]/2-MARGIN,-size[1]/2-MARGIN,-size[2]-MARGIN])
		{
			#cube(size=[size[0]+2*MARGIN,size[1]+2*MARGIN,size[2]+2*MARGIN], center=false);
			translate([-(encoderSize[0]-size[0])/2-DELTA,-(encoderSize[1]-size[1])/2-DELTA,0])
				#cube(size=[encoderSize[0]+2*MARGIN+2*DELTA,encoderSize[1]+2*MARGIN+2*DELTA,encoderSize[2]+2*MARGIN+2*DELTA], center=false);
		}
		#cylinder(d=shaftDiameter+2+2*MARGIN, h=0.7+MARGIN+(wallThickness), center=false, $fn=16);
		#cylinder(d=shaftDiameter+2*MARGIN, h=shaftLength+MARGIN, center=false, $fn=16);
		translate([size[1]/2,0,0])
			cube(size=[size[1],shaftDiameter+2*MARGIN,shaftLength+MARGIN], center=true);
		
		translate([0,4.5,0])
			#cylinder(d=1.6+MARGIN, h=wallThickness+MARGIN, center=false, $fn=8);
		translate([0,-4.5,0])
			#cylinder(d=1.6+MARGIN, h=wallThickness+MARGIN, center=false, $fn=8);
	}
}

module tensegrity_rod_actuator(internal_angle, rod_diameter, rod_length, actuator_angle, trim_angle)
{
	inverted_angle=(actuator_angle<0)?0:180;
	inverted_sign=(actuator_angle<0)?1:-1;
	motor_mount_height=12;
	motor_width=12;
	motor_mount_width=max(rod_diameter+DELTA,motor_width+2*MARGIN+DELTA);
	motor_mount_length=31;
	motor_mount_offset=motor_mount_length-rod_diameter/(abs(cos(actuator_angle)));
	motor_encoder_width=12;
	
	difference()
	{
		union()
		{
			//Rods for holding tension elements
			translate([-rod_diameter/2,-rod_diameter/2,-10])
				cube(size=[rod_diameter, rod_diameter, rod_length], center=false);
			
			//Support for front of motor mount
			translate([0,0,rod_length-(motor_mount_height+motor_mount_offset-rod_diameter-1)/(abs(cos(actuator_angle)))])
				rotate([0,actuator_angle,0])
					translate([inverted_sign*(motor_mount_offset*abs(sin(actuator_angle))-rod_diameter),0,rod_diameter/2])
						cube(size=[(motor_mount_height+motor_mount_offset)*abs(cos(actuator_angle)),rod_diameter,rod_diameter], center=true);

			//Loops for hooking springs and strings
			translate([spring_hook_diameter/2,0,rod_length])
				rotate([0,actuator_angle+90,0])
					hookToroid();
			translate([spring_hook_diameter/2,(motor_mount_width/2+spring_wire_diameter),rod_length-8.5])
				rotate([0,actuator_angle,0])
					hookToroid();
			translate([spring_hook_diameter/2,-(motor_mount_width/2+spring_wire_diameter),rod_length-8.5])
				rotate([0,actuator_angle,0])
					hookToroid();
		}
		//Cut off top of rod for an actuator mount
		translate([0,0,rod_length])
			rotate([0,actuator_angle,0])
				translate([-motor_mount_height/2,-motor_mount_width/2-DELTA,spring_wire_diameter/2-DELTA])
				{
					cube(size=[motor_mount_height+2*DELTA,motor_mount_width+2*DELTA,motor_mount_length+2*DELTA], center=false);
					translate([0,(motor_mount_width-motor_encoder_width)/2,0])
						cube(size=[motor_mount_height+2*DELTA,motor_encoder_width+2*DELTA,motor_mount_offset/2-3+2*DELTA], center=false);
				}

		//Cut off back of rod for fabrication
		translate([0,0,rod_length])
			rotate([0,trim_angle+180,0])
				translate([1.83841,-motor_mount_width/2-(spring_hook_diameter+spring_wire_diameter),motor_mount_offset-motor_mount_length])
					cube(size=[motor_mount_height,motor_mount_width+2*(spring_hook_diameter+spring_wire_diameter),motor_mount_length], center=false);
		
	}
	
	//Micro-motor mounts for body actuators
	translate([0,0,rod_length])
		rotate([0,actuator_angle,0])
			translate([0,0,motor_mount_offset+10])
				rotate([0,0,inverted_angle])
					motorMountMicro();
}

module tensegrity_rod_attachment(internal_angle, rod_diameter, rod_length, actuator_angle, trim_angle)
{
	motor_mount_height=12;
	motor_width=12;
	motor_mount_width=max(rod_diameter+DELTA,motor_width+2*MARGIN+DELTA);
	motor_mount_length=31;
	motor_mount_offset=motor_mount_length-rod_diameter/(abs(cos(actuator_angle)));
	spring_hook_diameter=7;
	spring_wire_diameter=3;
	
	difference()
	{
		union()
		{
			//Rods for holding tension elements
			translate([-rod_diameter/2,-rod_diameter/2,-10])
				cube(size=[rod_diameter, rod_diameter, rod_length], center=false);
			
			//Loops for hooking springs and strings
			translate([spring_hook_diameter/2,0,rod_length])
				rotate([0,actuator_angle+90,0])
					hookToroid();
			translate([spring_hook_diameter/2,(motor_mount_width/2+spring_wire_diameter),rod_length-8.5])
				rotate([0,actuator_angle,0])
					hookToroid();
			translate([spring_hook_diameter/2,-(motor_mount_width/2+spring_wire_diameter),rod_length-8.5])
				rotate([0,actuator_angle,0])
					hookToroid();
		}
		//Cut off back of rod for fabrication
		translate([0,0,rod_length])
			rotate([0,trim_angle+180,0])
				translate([1.83841,-motor_mount_width/2-(spring_hook_diameter+spring_wire_diameter),motor_mount_offset-motor_mount_length])
					cube(size=[motor_mount_height,motor_mount_width+2*(spring_hook_diameter+spring_wire_diameter),motor_mount_length], center=false);
		
	}
	
	//Micro-motor mounts for body actuators
	translate([0,0,rod_length])
		rotate([0,actuator_angle,0])
			translate([0,0,rod_diameter*2])
				sphere(r=rod_diameter);
}

module tensegrity_actuator_cubemount(internal_angle, rod_diameter, rod_length, internal_length_reduction, actuator)
{
	internal_length_reduction = CUBE_TILE_SIZE[0]*cos(internal_angle);
	actuator_angle=180-internal_angle;
	web_support_angle=8.9394;
	web_support_height=CUBE_TILE_SIZE[2]/2;
	web_support_thickness=WALL_THICKNESS;
	web_support_length=rod_length-internal_length_reduction+(CUBE_TILE_SIZE[2]-rod_diameter/2-web_support_height/2)*sin(internal_angle);
	web_support_camber=atan2(CUBE_TILE_SIZE[1]/2,web_support_length);
	
	echo("rotate([0,",internal_angle-180-web_support_angle,",0]) translate([-CUBE_TILE_SIZE[0]/2+CUBE_TILE_SIZE[2],0,-CUBE_TILE_SIZE[0]/2-WALL_THICKNESS/2-MARGIN/5]) tensegrity_actuator_cubemount(",internal_angle, rod_diameter, rod_length, internal_length_reduction, actuator,");");
	
	//Mounting brackets for rods to modules
	difference()
	{
		union()
		{
			//Tensegrity compression rod and actuator
			rotate([0,internal_angle,0])
				translate([0,0,internal_length_reduction])
				{
					if(actuator)
						tensegrity_rod_actuator(internal_angle=internal_angle, rod_diameter=rod_diameter, rod_length=rod_length-internal_length_reduction, actuator_angle=actuator_angle, trim_angle=web_support_angle);
					else
						tensegrity_rod_attachment(internal_angle=internal_angle, rod_diameter=rod_diameter, rod_length=rod_length-internal_length_reduction, actuator_angle=actuator_angle, trim_angle=web_support_angle);
				}
			
			difference()
			{
				union()
				{
					//Additional web for support of compression rod
					//Edge to assist 3D printing from base
					translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS*cos(internal_angle),-CUBE_TILE_SIZE[1]/2-WALL_THICKNESS,CUBE_TILE_SIZE[0]/2])
						rotate([0,internal_angle+web_support_angle,0])
							cube(size=[5,CUBE_TILE_SIZE[1]+2*WALL_THICKNESS,5]);
					//Central web section
					translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS*cos(internal_angle),-web_support_thickness/2,CUBE_TILE_SIZE[0]/2])
						rotate([0,internal_angle+web_support_angle,0])
						{
							cube(size=[web_support_height,web_support_thickness,(web_support_length)/cos(web_support_angle)]);
							difference()
							{
								rotate([0,90-internal_angle-web_support_angle,0])
									translate([0,web_support_thickness/2,0])
										cylinder(d=web_support_length/8,h=CUBE_TILE_SIZE[2]);
								
								translate([-web_support_length/8,-web_support_length/16+web_support_thickness/2,0])
									cube(size=[web_support_length/8+DELTA,web_support_length/8,web_support_length/8]);
							}
						}
					//Side web section
					translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS*cos(internal_angle),CUBE_TILE_SIZE[1]/2-web_support_thickness/2,CUBE_TILE_SIZE[0]/2])
						rotate([0,internal_angle+web_support_angle,0])
							rotate([web_support_camber,0,0])
							{
								cube(size=[web_support_height,web_support_thickness,(web_support_length)/cos(web_support_camber)]);
								difference()
								{
									rotate([0,90-internal_angle-web_support_angle,0])
										translate([0,web_support_thickness/2,0])
											cylinder(d=web_support_length/8,h=CUBE_TILE_SIZE[2]);
									
									translate([-web_support_length/8,-web_support_length/16+web_support_thickness/2,0])
										cube(size=[web_support_length/8+DELTA,web_support_length/8,web_support_length/8]);
								}
							}
					//Side web section
					translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS*cos(internal_angle),-(CUBE_TILE_SIZE[1]/2+web_support_thickness/2),CUBE_TILE_SIZE[0]/2])
						rotate([0,internal_angle+web_support_angle,0])
							rotate([-web_support_camber,0,0])
							{
								cube(size=[web_support_height,web_support_thickness,(web_support_length)/cos(web_support_camber)]);
								difference()
								{
									rotate([0,90-internal_angle-web_support_angle,0])
										translate([0,web_support_thickness/2,0])
											cylinder(d=web_support_length/8,h=CUBE_TILE_SIZE[2]);
									
									translate([-web_support_length/8,-web_support_length/16+web_support_thickness/2,0])
										cube(size=[web_support_length/8+DELTA,web_support_length/8,web_support_length/8]);
								}
							}
				}
			
				//Space that the actuator takes up
				rotate([0,internal_angle,0])
					translate([0,-CUBE_TILE_SIZE[1]/2,rod_length])
						rotate([0,actuator_angle-90,0])
							translate([0,0,-CUBE_TILE_SIZE[2]*sin(internal_angle)/2])
								cube(size=CUBE_TILE_SIZE, center=false);
			}
			
			//Bracket around edge of module
			translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]/2+WALL_THICKNESS-MARGIN,0,CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]/2+WALL_THICKNESS-MARGIN])
					cube(size=[CUBE_TILE_SIZE[2],CUBE_TILE_SIZE[0]-2*CUBE_TILE_SIZE[2]+WALL_THICKNESS*4+MARGIN*4-DELTA,CUBE_TILE_SIZE[2]], center=true);
		}
		
		//Space that the module takes up
		translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]/2,0,CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]/2])
		{
			cube(size=[CUBE_TILE_SIZE[2],CUBE_TILE_SIZE[0]-2*CUBE_TILE_SIZE[2]+WALL_THICKNESS*4+MARGIN*4+DELTA,CUBE_TILE_SIZE[2]], center=true);
			translate([-CUBE_TILE_SIZE[2]+WALL_THICKNESS-MARGIN+DELTA,0,CUBE_TILE_SIZE[2]/2])
				cube(size=[CUBE_TILE_SIZE[2],CUBE_TILE_SIZE[0]-2*CUBE_TILE_SIZE[2]+WALL_THICKNESS*4+MARGIN*4+DELTA,CUBE_TILE_SIZE[2]], center=true);
			translate([CUBE_TILE_SIZE[2]/2,0,-CUBE_TILE_SIZE[2]+WALL_THICKNESS-MARGIN+DELTA])
				cube(size=[CUBE_TILE_SIZE[2],CUBE_TILE_SIZE[0]-2*CUBE_TILE_SIZE[2]+WALL_THICKNESS*4+MARGIN*4+DELTA,CUBE_TILE_SIZE[2]], center=true);
		}

	}
	
	//Angle tab for connection to module
	dual_mirror([0,1,0])
		rotate([-90,0,90])
			translate([WALL_THICKNESS+MARGIN,-CUBE_TILE_SIZE[0]+CUBE_TILE_SIZE[2],-CUBE_TILE_SIZE[0]/2+CUBE_TILE_SIZE[2]/2])
			{
				cubetiletab(size=CUBE_TILE_SIZE, wall_thickness=WALL_THICKNESS, screw_diameter_chassis=SCREW_DIAMETER_CHASSIS);
				translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]+MARGIN-DELTA,CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS/2,-CUBE_TILE_SIZE[2]/2-WALL_THICKNESS/2-MARGIN])
					cube(size=[WALL_THICKNESS+2*DELTA,WALL_THICKNESS,CUBE_TILE_SIZE[2]-WALL_THICKNESS*3/2-MARGIN+2*DELTA]);
				translate([CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]+MARGIN-DELTA,CUBE_TILE_SIZE[0]/2-CUBE_TILE_SIZE[2]-WALL_THICKNESS/2-MARGIN,-CUBE_TILE_SIZE[2]/2-WALL_THICKNESS/2-MARGIN])
					cube(size=[WALL_THICKNESS+2*DELTA,CUBE_TILE_SIZE[2]-WALL_THICKNESS*3/2-MARGIN+2*DELTA,WALL_THICKNESS]);
			}
}

module tensegrity_rod_pair(internal_angle, rod_diameter, rod_length)
{
	rotate([0,internal_angle])
		translate([3,0,0])
			cylinder(h=rod_length, d=rod_diameter, center=false, $fn=32);
	rotate([0,-internal_angle,0])
		translate([-3,0,0])
			cylinder(h=rod_length, d=rod_diameter, center=false, $fn=32);
}

module tensegrity_tetrahedral_hub(hub_size, internal_angle, rod_diameter, rod_length, axial_rotation)
{
	echo("tensegrity_tetrahedral_hub(",hub_size, internal_angle, rod_diameter, rod_length, axial_rotation,");");
	
	difference()
	{
		rotate([0,0,45])
			cube(size=[hub_size, hub_size, hub_size], center=true);
		
		tensegrity_rod_pair(internal_angle, rod_diameter, hub_size);
		
		rotate([0,internal_angle,0])
			translate([-hub_size/2,-hub_size/2,hub_size/4+hub_size*cos(internal_angle)/2])
				cube(size=[hub_size, hub_size, hub_size], center=false);
		rotate([0,-internal_angle,0])
			translate([-hub_size/2,-hub_size/2,hub_size/4+hub_size*cos(internal_angle)/2])
				cube(size=[hub_size, hub_size, hub_size], center=false);
		
		rotate([0,180,axial_rotation])
		{
			tensegrity_rod_pair(internal_angle, rod_diameter, hub_size);
			
			rotate([0,internal_angle,0])
				translate([-hub_size/2,-hub_size/2,hub_size/4+hub_size*cos(internal_angle)/2])
					cube(size=[hub_size, hub_size, hub_size], center=false);
			rotate([0,-internal_angle,0])
				translate([-hub_size/2,-hub_size/2,hub_size/4+hub_size*cos(internal_angle)/2])
					cube(size=[hub_size, hub_size, hub_size], center=false);
		}
	}
}

module tensegrity_tetrahedral_module(type, hub_size, internal_angle, rod_diameter, rod_length, axial_rotation, actuators)
{
	//System Elements
	//#cubemodhull();
	if(type == 10)
		cubeModAssemble(types=[10,10,10,10,10,10],location=[0, 0, 0]);
	if(type == 19)
		cubeModAssemble(types=[10,10,10,10,90,90],location=[0, 0, 0]);
	
	dual_mirror([1,0,0])
		tensegrity_actuator_cubemount(internal_angle, rod_diameter, rod_length, CUBE_TILE_SIZE[0]*cos(internal_angle), actuators);
	rotate([0,180,axial_rotation])
		dual_mirror([1,0,0])
			tensegrity_actuator_cubemount(internal_angle, rod_diameter, rod_length, CUBE_TILE_SIZE[0]*cos(internal_angle), actuators);
}

module tensegrity_tetrahedral_spine_element(type, hub_size, internal_angle, rod_diameter, rod_length, planar)
{
	echo("tensegrity_tetrahedral_spine_element(",type, hub_size, internal_angle, rod_diameter, rod_length, planar,");");
	
	axial_rotation=(planar)?0:90;
	actuators=(planar)?false:true;

	//Specific form factors for types of elements
	if (type == 0) //Cube hub and rods (structure-only)
	{
		tensegrity_tetrahedral_hub(hub_size, internal_angle, rod_diameter, rod_length, axial_rotation);

		%tensegrity_rod_pair(internal_angle, rod_diameter, rod_length, 0, 16);
		rotate([0,0,axial_rotation])
			%tensegrity_rod_pair(internal_angle+180, rod_diameter, rod_length, 0, 16);
	}
	else //Module mounts using cubemodule tiles
	{
		hub_size=100;
		tensegrity_tetrahedral_module(type, hub_size, internal_angle, rod_diameter, rod_length, axial_rotation, actuators);
	}
}

module tensegrity_tetrahedral_drive_axle(internal_angle, rod_diameter, rod_length, actuators=false)
{
	axle_diameter=rod_diameter*2;
	
	echo("tensegrity_tetrahedral_drive_axle(",internal_angle, rod_diameter, rod_length, actuators,");");

	difference()
	{
		union()
		{
			rotate([90, 90, 0])
				cube(size=[axle_diameter, axle_diameter, rod_length/cos(internal_angle)], center=true);

			//Tension spring hooks
			hookOffset = rod_length*cos(internal_angle)-SCREW_DIAMETER_CHASSIS*2;
			for(hookPosition = [hookOffset, -hookOffset])
			{
				translate([-axle_diameter/2-SCREW_DIAMETER_CHASSIS, hookPosition, 0])
					hookToroid();
				translate([0, hookPosition, -axle_diameter+SCREW_DIAMETER_CHASSIS])
						if(actuators)
						{
							rotate([0,180,0])
								translate([0,0,32])
									motorMountMicro();
							translate([8,-10,-30])
								difference()
								{
									cube([20,18,30]);
									rotate([0,45,0])
										translate([0,-DELTA,0])
											cube([20+DELTA,18+2*DELTA,30+DELTA]);
								}
						}
						else
							rotate([90, 0, 0])
								hookToroid();
				translate([motor_outer_diameter+axle_diameter+WALL_THICKNESS/2, hookPosition*cos(internal_angle), 0])
					hookToroid();
			}

			//Wheel location
			for(wheelAngle = [-90, 90])
				rotate([wheelAngle, 0, 0])
					translate([motor_outer_diameter/2+axle_diameter/2, 0, 0])
					{
						translate([0, 0, rod_length*cos(internal_angle)-motor_outer_length+WALL_THICKNESS])
							cylinder(d=motor_outer_diameter+2*WALL_THICKNESS, h=motor_outer_length+WALL_THICKNESS);
						translate([9, 0, rod_length*cos(internal_angle)+WALL_THICKNESS+6])
							wheelFlat();
					}
		}

		for(wheelAngle = [-90, 90])
			rotate([wheelAngle, 0, 0])
				translate([motor_outer_diameter/2+axle_diameter/2+MARGIN, 0, 0])
				{
					//Motor hull
					translate([0, 0, rod_length*cos(internal_angle)-motor_outer_length-MARGIN])
						cylinder(d=motor_outer_diameter+2*MARGIN, h=motor_outer_length+WALL_THICKNESS+MARGIN);

					//Motor
					translate([0, 0, rod_length*cos(internal_angle)-motor_outer_length])
						rotate([0,0,180])
							#zchxd_motor();
                    
                    //Cutaway for access
					rotate([0,60,0])
						translate([-motor_outer_length/4+7,0,motor_outer_diameter])
							cube(size=[motor_outer_diameter+2*WALL_THICKNESS+2*DELTA, motor_outer_diameter+2*WALL_THICKNESS+2*DELTA, motor_outer_length], center=true);
				}
	}
}

module tensegrity_tetrahedral_spine(type=[0,0,0], num_elements=3, hub_size=25.4, internal_angle=45, rod_diameter=6, rod_length=150)
{
	spring_diameter_outer = 5;
	spring_diameter_inner = 8;
	element_separation = 2*rod_length*cos(internal_angle);

	for(element = [0:num_elements-1])
	{
		translate([-element*element_separation, 0, 0])
		{
			rotate([0, 90, 0])
			{
				//Elements themselves - the last one needs to be planar
				if(element == num_elements-1)
					tensegrity_tetrahedral_spine_element(type[element], hub_size, internal_angle, rod_diameter, rod_length, true);
				
				if(element == 0)
					tensegrity_tetrahedral_spine_element(type[element], hub_size, internal_angle, rod_diameter, rod_length, false);
				
				if(element > 0 && element < num_elements-1)
				{
					tensegrity_tetrahedral_spine_element(type[element], hub_size, internal_angle, rod_diameter, rod_length, false);
					for(wheelAngle = [-90, 90])
						rotate([wheelAngle, 0, 0])
							translate([39, 0, rod_length*cos(internal_angle)+20])
								wheelFlat();
				}
				
				//Front and Back motors are on their own rods (axles)
				//front_offset=(element==0)?+motor_offset:0;
				//back_offset=(element==num_elements-1)?-motor_offset:0;
				//translate([0,0,front_offset+back_offset])
				if(element == 0)
					translate([5, 0, element_separation/2])
						tensegrity_tetrahedral_drive_axle(internal_angle, rod_diameter, rod_length, false);
				if(element == num_elements-1)
					translate([5, 0, -element_separation/2])
						rotate([180,0,0])
							tensegrity_tetrahedral_drive_axle(internal_angle, rod_diameter, rod_length, true);
			
				//Springs connecting elements
				for(elementAngle = [0, 90])
				{
					rotate([0, 0, elementAngle])
					{
						for(rodAngle = [internal_angle, -internal_angle])
						{
							rotate([0, rodAngle, 0])
								translate([0, 0, rod_length])
								{
									//Outer Springs
									rotate([0, 180-rodAngle, 0])
										translate([0, 0, 10])
											if(element < num_elements-1)
												%cylinder(r=1, h=element_separation-20);
												//%coil(r1=spring_diameter_outer, r2=spring_diameter_outer/10, h=element_separation-20, n=element_separation/spring_diameter_outer/2);
									
									//Inner Springs
									rotate([180-rodAngle, rodAngle, 0])
										translate([0, 0, 10])
											//%cylinder(r=2, h=element_separation*cos(internal_angle)-20);
											%coil(r1=spring_diameter_inner, r2=spring_diameter_inner/10, h=element_separation*cos(internal_angle)-20, n=element_separation/spring_diameter_inner);
									
									//Inner springs at end
									if(element == num_elements-1)
									{
											rotate([180-rodAngle, rodAngle, 0])
												translate([element_separation, 0, 10])
													//%cylinder(r=2, h=element_separation*cos(internal_angle)-20);
													%coil(r1=spring_diameter_inner, r2=spring_diameter_inner/10, h=element_separation*cos(internal_angle)-20, n=element_separation/spring_diameter_inner);
									}
								}
						}
					}
				}
			}
		}
	}
}

tensegrity_tetrahedral_spine(type=[10,19,10], num_elements=3, hub_size=25.4, internal_angle=45, rod_diameter=6, rod_length=140);

//tensegrity_tetrahedral_hub(25.4, 45, 6, 120, 90);

//tensegrity_tetrahedral_drive_axle(45, 6, 140, true);

//rotate([0,0,90]) wheelFlat(200, 30, 30, 6, 12, 5, 10, 4);

//rotate([0, -143.939, 0]) translate([-CUBE_TILE_SIZE[0]/2+CUBE_TILE_SIZE[2],0,-CUBE_TILE_SIZE[0]/2-WALL_THICKNESS/2-MARGIN/5]) tensegrity_actuator_cubemount(45, 6, 140, 70.7107, true);

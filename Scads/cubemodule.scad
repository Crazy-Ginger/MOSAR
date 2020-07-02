//Tiny variation to differentiate planes at same location
DELTA=0.01;
//Size margin for expansion of rapid prototyped parts
MARGIN=0.2;
//Standard parameters for cube module
CUBE_TILE_SIZE=[100, 60, 20];
WALL_THICKNESS=2;
SCREW_DIAMETER_CHASSIS=3;

include <zchxd_motor.scad>;

module springContact(mountDiameter=5, mountDistance=3, baseDiameter=1.828, baseHeight=0.41, bodyDiameter=1.625, bodyHeight=0.71, headDiameter=1.7, headHeight=0.81, pinDiameter=1.067, pinHeight=0.61)
{
	//Spring pin part# MILL MAX 0965-0-15-20-80-14-11-0
	union()
	{
		translate([0, 0, -pinHeight-MARGIN])
		{
			#cylinder(h=pinHeight+MARGIN, d=pinDiameter+2*MARGIN, center=false, $fn=8);
			translate([0, 0, pinHeight+MARGIN-DELTA])
			{
				#cylinder(h=headHeight+MARGIN+DELTA, d=headDiameter+2*MARGIN, center=false, $fn=8);
				translate([0, 0, headHeight-MARGIN])
				{
					#cylinder(h=bodyHeight+2*MARGIN+DELTA, d=bodyDiameter+2*MARGIN, center=false, $fn=8);
					translate([0, 0, bodyHeight+2*MARGIN])
					{
						#cylinder(h=baseHeight+MARGIN+DELTA, d=baseDiameter+2*MARGIN, center=false, $fn=8);
						translate([0, 0, baseHeight+MARGIN])
						{
							//Hole for mounting access
							cylinder(h=mountDistance+MARGIN+DELTA, d=mountDiameter+2*MARGIN, center=false, $fn=8);
						}
					}
				}
			}
		}
	}
}

module magnet(magnet_diameter, magnet_depth, wiring_diameter, wiring_depth)
{
	//Magnet space with additional mounting space at bottom
	wireConnectHeight=0.3;
	wireConnectDiameter=5;
	//TODO: apply chamfer to magnet
	#cylinder(h=magnet_depth+MARGIN, d=magnet_diameter+2*MARGIN, center=false);
	translate([0, 0, magnet_depth+MARGIN-DELTA])
	{
		cylinder(h=wireConnectHeight+MARGIN+2*DELTA, d=wireConnectDiameter+2*MARGIN, center=false);
		translate([0, 0, wireConnectHeight+MARGIN-DELTA])
			cylinder(h=wiring_depth-magnet_depth-wireConnectHeight+2*DELTA, d=wiring_diameter+2*MARGIN, center=false);
	}
}

module nutmount(containerHeight, boltDiameter=3, flushTop=false)
{
	//Rough calculation for exterior of small fasteners
	nutDiameter=2*boltDiameter+0.5-MARGIN;
	nutHeight=boltDiameter-0.5;
	flushOffset=(flushTop)?0:nutHeight;
	flushShorten=(flushTop)?nutHeight:0;

	//Bolt hole, nut recess and standoff for mounting
	translate([0, 0, -flushOffset-DELTA])
	{
		#cylinder(h=nutHeight+MARGIN, d=nutDiameter+2*MARGIN, center=false, $fn=6);
		translate([0, 0, nutHeight-DELTA])
			#cylinder(h=containerHeight-flushShorten+2*DELTA, d=boltDiameter+2*MARGIN, center=false, $fn=8);
	}
}
 
module ir_transceiver()
{
	//IR transceiver model
	translate([-MARGIN, -MARGIN, -1.65/2-MARGIN])
	{
		cube([6+2*MARGIN, 1.9+2*MARGIN, 1.65+2*MARGIN], center=true);
		translate([3.81/2, 0, -1.65/2+DELTA])
			sphere(r=3-1.65+MARGIN, $fn=8);
		translate([-3.81/2, 0, -1.65/2+DELTA])
			sphere(r=2.745-1.65+MARGIN, $fn=8);
	}
}

module board_volume_RPiZero(container_height, wall_thickness, board_thickness)
{
	//Import actual model of Pi 3B+
	translate([85,56,0]) rotate([0,0,180])
	{
		rotate([-90,0,0]) %import("RaspberryPiZeroW.stl", convexity=3);
	
		//Approximate volume of Pi Zero
		translate([0, 0, -5])
			cube([66, 30, 6+DELTA], center=false);
	
		//Approximate volume of Pi hat with transceiver
		translate([0, 0, -board_thickness-1.5-11.7])
		{
			%cube([65, 56, 4.5], center=false);
			translate([65/2+4.5, 56/2, -1.65/2-DELTA])
				#ir_transceiver();
		}

		//Board notches
		translate([-0.5-MARGIN, -0.5-MARGIN, -board_thickness-MARGIN])
			cube([86+2*MARGIN, 57+2*MARGIN, board_thickness+2*MARGIN], center=false);
		translate([-0.5-MARGIN, -0.5-MARGIN, -board_thickness-MARGIN-1.5-11.7])
			cube([65.5+2*MARGIN, 57+2*MARGIN, board_thickness+2*MARGIN], center=false);
		
		//Bolt holes and nut recesses for mounting
		for (x=[3.5,3.5+58])
			for (y=[3.5,3.5+49]) 
				translate([x, y, -container_height])
					nutmount(container_height+1, boltDiameter=2.5, flushTop=true);
	}

	//Openings for connectors
	//SD Card and removal hole
	translate([71.5-DELTA, 36.5-MARGIN, DELTA])
	{
		cube([30, 12.5+2*MARGIN, 1.7+DELTA+MARGIN], center=false);
		translate([14, 0, -1.5])
			cube([16, 12.5+2*MARGIN, 1.5+DELTA], center=false);
		translate([14, 6+MARGIN-2.5, -5])
			cube([16, 5.5, 3.5], center=false);
	}
	//Camera
	translate([10-MARGIN, 30-MARGIN, -3-MARGIN])
		cube([11+2*MARGIN, 20+2*MARGIN, 3+2*MARGIN], center=false);
	//Side connectors
	translate([27-MARGIN, 23-DELTA, -5+DELTA-MARGIN]) 
		cube([51+2*MARGIN, 3.5, 5], center=false);

	//Extra space in interior at ends
	translate([85, +DELTA, -container_height+wall_thickness+DELTA])
		cube([85/2-56/2-wall_thickness-DELTA, 56-2*DELTA, container_height-wall_thickness-DELTA], center=false);
	translate([0, +DELTA, -container_height+wall_thickness+DELTA])
		cube([85/2-56/2-wall_thickness-DELTA, 56-2*DELTA, container_height-wall_thickness-DELTA], center=false);

}

module board_volume_RPi(container_height, wall_thickness, board_thickness)
{
	//Import actual model of Pi 3B+
	translate([85,56,0]) rotate([0,0,180])
	{
		rotate([-90,0,0]) scale(25.4) %import("Rpi3Bplus.stl", convexity=3);
	
		//Approximate volume of Pi 3B+
		translate([0, 0, -10])
			cube([85, 56, 11+DELTA], center=false);
	
		//Approximate volume of Pi hat with transceiver
		translate([0, 0, -board_thickness-1.5-11.7])
		{
			%cube([65, 56, 4.5], center=false);
			translate([65/2+4.5, 56/2, -1.65/2-DELTA])
				#ir_transceiver();
		}

		//Board notches
		translate([-0.5-MARGIN, -0.5-MARGIN, -board_thickness-MARGIN])
			cube([86, 57, board_thickness+MARGIN], center=false);
		translate([-0.5-MARGIN, -0.5-MARGIN, -board_thickness-1.5-11.7-MARGIN])
			cube([65.5+2*MARGIN, 57+2*MARGIN, board_thickness+2*MARGIN], center=false);
		
		//Bolt holes and nut recesses for mounting
		for (x=[3.5,3.5+58])
			for (y=[3.5,3.5+49]) 
				translate([x, y, -container_height])
					nutmount(container_height+1, boltDiameter=2.5, flushTop=true);
	}

	//Openings for connectors
	//SD Card and removal hole
	translate([71.5-DELTA, 22-MARGIN, -DELTA])
	{
		cube([30, 12+2*MARGIN, 1.5+DELTA+MARGIN], center=false);
		translate([14, 0, -1.5])
			cube([16, 12+2*MARGIN, 1.5+DELTA], center=false);
		translate([14, 6+MARGIN-2.5, -5])
			cube([16, 5, 3.5], center=false);
	}
	translate([-1-DELTA, 1, -18+DELTA])
	{
		//Ethernet
		cube([21, 20+DELTA, 19], center=false);
		translate([-1+DELTA, 0, 2])
			cube([1, 20, 17], center=false);
	}
	translate([-2-DELTA,21,-18-2*DELTA])
	{
		//USB
		cube([22, 33, 19+3*DELTA], center=false);
		translate([0, -1, -1+DELTA])
			cube([1+DELTA, 36, 20+2*DELTA], center=false);
	}
	//Side connectors
	translate([28-MARGIN, -8-MARGIN, -8-MARGIN]) 
		cube([50.5+2*MARGIN, 19.5, 9+2*MARGIN+DELTA], center=false);

	//Extra space in interior at end
	translate([85, +DELTA, -container_height+wall_thickness+DELTA])
		cube([85/2-56/2-wall_thickness-DELTA, 56-2*DELTA, container_height-wall_thickness-DELTA], center=false);

}

module cubetilecontents(type, size, wall_thickness, board_size, board_thickness, board_back_clearance, board_mount_inset, screw_diameter_mounting, connector_depth, interface_diameter)
{
			//Specific form factors for types of tiles
			if (abs(type) == 10)  //Generic embedded board tile
			{
				boardToTop=connector_depth+board_back_clearance+board_thickness+DELTA;
				translate([0, 0, -size[2]/2+boardToTop-board_thickness/2])
				{
					cube([board_size[0]+1+2*DELTA, board_size[1]+1+2*DELTA, board_thickness+2*DELTA], center=true);
					translate([0, 0, -board_thickness/2-2*DELTA])
						#ir_transceiver();
				}
				quad_mirror()
					translate([size[0]/2-wall_thickness-board_mount_inset, size[1]/2-wall_thickness-board_mount_inset, -size[2]/2])
						nutmount(boardToTop, screw_diameter_mounting, flushTop=true);
			}
			if (abs(type) == 20)  //Pi Zero embedded board tile
			{
				translate([-size[0]/2+wall_thickness-DELTA, -size[1]/2+wall_thickness, size[2]/2-1])
					board_volume_RPiZero(size[2]-1, wall_thickness=wall_thickness, board_thickness=board_thickness);
			}
			if (abs(type) == 30)  //Pi 3B+ tile
			{
				translate([-size[0]/2+wall_thickness-DELTA, -size[1]/2+wall_thickness, size[2]/2-1])
					board_volume_RPi(size[2]-1, wall_thickness=wall_thickness, board_thickness=board_thickness);
			}
			if (abs(type) == 40)  //Battery and power management tile
			{
				boardToTop=connector_depth+board_back_clearance+board_thickness+DELTA;
				translate([0, 0, -size[2]/2+boardToTop-board_thickness/2])
				{
					cube([board_size[0]+1+2*DELTA, board_size[1]+1+2*DELTA, board_thickness+2*DELTA], center=true);
					translate([0, 0, -board_thickness/2-2*DELTA])
						#ir_transceiver();
				}
				quad_mirror()
					translate([size[0]/2-wall_thickness-board_mount_inset, size[1]/2-wall_thickness-board_mount_inset, -size[2]/2])
						nutmount(boardToTop, screw_diameter_mounting, flushTop=true);
			}
			if (abs(type) == 50)  //Sensor Tile
			{
				boardToTop=connector_depth+board_back_clearance+board_thickness+DELTA;
				translate([0, 0, -size[2]/2+boardToTop-board_thickness/2])
				{
					cube([board_size[0]+1+2*DELTA, board_size[1]+1+2*DELTA, board_thickness+2*DELTA], center=true);
					translate([0, 0, -board_thickness/2-2*DELTA])
						#ir_transceiver();
				}
				quad_mirror()
					translate([size[0]/2-wall_thickness-board_mount_inset, size[1]/2-wall_thickness-board_mount_inset, -size[2]/2])
						nutmount(boardToTop, screw_diameter_mounting, flushTop=true);
			}
			if (abs(type) == 80)  //Motor rotation tile
			{
				translate([-size[0]/2+wall_thickness-DELTA, -size[1]/2+wall_thickness-DELTA, size[2]/2-DELTA])
					translate([0, 0, -wall_thickness-board_thickness])
					#cube([36+1+2*DELTA, 56+1+2*DELTA, board_thickness+2*DELTA+MARGIN], center=false);
			}
			if (abs(type) == 90)  //Drive Wheel Tile
			{
				boardToTop=connector_depth+board_back_clearance+board_thickness+DELTA;
				translate([0, 0, -size[2]/2+boardToTop-board_thickness/2])
				{
					translate([-size[0]*2/12+board_thickness+DELTA,0,0])
						#cube([size[0]*2/3, board_size[1]+1+2*DELTA, board_thickness+2*DELTA], center=true);
					translate([0, 0, -board_thickness/2-2*DELTA])
						#ir_transceiver();
				}
				dual_mirror([0,1,0])
					translate([-(size[0]/2-wall_thickness-board_mount_inset), size[1]/2-wall_thickness-board_mount_inset, -size[2]/2])
						nutmount(boardToTop, screw_diameter_mounting, flushTop=true);
				
				translate([size[0]/2-motor_outer_diameter/2-wall_thickness-MARGIN,0,wall_thickness])
					rotate([0,180,0])
						#zchxd_motor();
			}
}

module modconnector(connector_diameter=60, connector_depth=5, pin_separation=3, magnet_separation=50, magnet_diameter=8, magnet_depth=3, wiring_diameter=3, LED_diameter=3, interface_diameter=10)
{
	//Outline of rotating connector
	%difference()
	{
		cylinder(h=connector_depth, d=connector_diameter, center=false);
		translate([0, 0, -DELTA])
		cylinder(h=connector_depth+2*DELTA, d=interface_diameter+2*MARGIN, center=false);
	}

	//Hole for optical interface and other inter-module components
	translate([0, 0, -DELTA])
		cylinder(h=connector_depth+2*DELTA, d=interface_diameter+2*MARGIN, center=false);
	
	//Holes for spring contacts for power connectors
	for (angle_offset=[0:90:360-90])
	{
		rotate([0,0,angle_offset]) translate([diametric_offset, 0, -DELTA])
			springContact();
		rotate([0,0,angle_offset]) translate([diametric_offset-pin_separation, 0, -DELTA])
			springContact();
	}

	//Holes for magnets as data connectors with wiring holes
	diametric_offset=magnet_separation/2;
	for (angle_offset=[22.5:45:360-22.5])
		rotate([0,0,angle_offset]) translate([diametric_offset, 0, -DELTA])
			magnet(magnet_diameter=magnet_diameter, magnet_depth=magnet_depth, wiring_diameter=wiring_diameter
, wiring_depth=connector_depth);

	//Holes for 3mm LED indicators and wiring
	for (x=[-30, 30])
		for (y=[20, -20]) 
			translate([x, y, -DELTA])
				#cylinder(h=connector_depth+2*DELTA, d=LED_diameter+2*MARGIN, center=false, $fn=8);
}

module cubetiletab(size, wall_thickness, screw_diameter_chassis)
{
	translate([size[0]/2-size[2]/2, size[1]/2+size[2]/2, 0])
	{
		rotate([0, -90, 0]) //remove this operation for connectors on bottom of tile
		difference()
		{
			translate([-wall_thickness-MARGIN, -wall_thickness-MARGIN, size[2]/2-wall_thickness/2-MARGIN])
				//we only need to back off -wall_thickness in X but we back off -2*wall_thickness just for extra space
				cube([size[2]-2*wall_thickness-2*MARGIN, size[2]-2*wall_thickness-2*MARGIN+2*DELTA, wall_thickness], center=true);
			translate([0, 0, size[2]/2-wall_thickness/2-MARGIN])
				//we should allow 2*MARGIN in diameters generally but here we only add MARGIN for a tight fit of countersunk bolts
				cylinder(h=wall_thickness+2*DELTA, d1=2*screw_diameter_chassis+MARGIN, d2=screw_diameter_chassis+MARGIN, center=true);
		}
	}
}

module cubetilehull(type, size, wall_thickness, screw_diameter_chassis)
{
	union()
	{
		//Tile hull
		cube(size, center=true);

		//Add right angle tabs for connection to other tiles
		if(type >= 0)
			quad_mirror()
				cubetiletab(size=size, wall_thickness=wall_thickness, screw_diameter_chassis=screw_diameter_chassis);
		
		//Add motor mount to drive motor tile
		if(type == 90)
		{
			translate([size[0]/2-motor_outer_diameter/2-wall_thickness-MARGIN,0,-motor_outer_length/2-wall_thickness-DELTA])
				cylinder(d=motor_outer_diameter+2*wall_thickness, h=motor_outer_length+wall_thickness, center=true);
		}
	}
}

module cubetile(type, size=CUBE_TILE_SIZE, wall_thickness=WALL_THICKNESS, screw_diameter_chassis=SCREW_DIAMETER_CHASSIS, board_size=[96, 56, 16], board_thickness=1.5, board_back_clearance=1, board_mount_inset=3.5, screw_diameter_mounting=3, connector_depth=5, pin_separation=3, magnet_separation=50, magnet_diameter=8, magnet_depth=3, wiring_diameter=6, LED_diameter=3, interface_diameter=10)
{
	//Centre tile coordinates on face of connector
	translate([0, 0, size[2]/2])
	{

		//Cut out tile by creating standard hull and then removing space for components
		difference()
		{
			//Solid tile form factor
			cubetilehull(type=type, size=size, wall_thickness=wall_thickness, screw_diameter_chassis=screw_diameter_chassis);
			
			//Connector for side of tile
			translate([0, 0, -size[2]/2-DELTA])
				modconnector(connector_diameter=size[1], connector_depth=connector_depth, pin_separation=pin_separation, magnet_separation=magnet_separation, magnet_diameter=magnet_diameter, magnet_depth=magnet_depth, wiring_diameter=wiring_diameter, LED_diameter=LED_diameter, interface_diameter=interface_diameter);
			
			//Clear volume inside tile
			difference()
			{
				//General space inside tile
				translate([-size[0]/2+wall_thickness, -size[1]/2+wall_thickness, -size[2]/2+connector_depth-2*DELTA])
					cube([size[0]-2*wall_thickness, size[1]-2*wall_thickness, size[2]-connector_depth+3*DELTA], center=false);
				//Add standoffs at corners
				quad_mirror()
					translate([size[0]/2-wall_thickness-board_mount_inset, size[1]/2-wall_thickness-board_mount_inset, -size[2]/2+connector_depth-3*DELTA])
						cylinder(h=board_back_clearance+2*DELTA, d=2*screw_diameter_mounting-2*MARGIN, center=false);
				//Add extra support around nuts at corners
				quad_mirror()
					translate([size[0]/2-size[2]/2+DELTA, size[1]/2-wall_thickness, board_back_clearance])
						rotate([-90, 0, 0])
							#cube([screw_diameter_chassis*3,screw_diameter_chassis*2,screw_diameter_chassis-0.5], center=true);

			}
			//Additional space at ends
			translate([-size[0]/2+wall_thickness, -size[1]/2+wall_thickness+3*screw_diameter_mounting, -size[2]/2+wall_thickness])
				cube([size[0]/2-size[1]/2-2*wall_thickness, size[1]-2*wall_thickness-6*screw_diameter_mounting, size[2]-wall_thickness+3*DELTA], center=false);
			translate([size[0]/2-wall_thickness-(size[0]/2-size[1]/2-2*wall_thickness), -size[1]/2+wall_thickness+3*screw_diameter_mounting, -size[2]/2+wall_thickness])
				cube([size[0]/2-size[1]/2-2*wall_thickness, size[1]-2*wall_thickness-6*screw_diameter_mounting, size[2]-wall_thickness+3*DELTA], center=false);
			
			//Place contents inside tile
			cubetilecontents(type=type, size=size, wall_thickness=wall_thickness, board_size=board_size, board_thickness=board_thickness, board_back_clearance=board_back_clearance, board_mount_inset=board_mount_inset, screw_diameter_mounting=screw_diameter_mounting, connector_depth=connector_depth, interface_diameter=interface_diameter);
			
			//Make extra space at top of tile if there is no mechanical complexity needed there
			if (type != 10)  //Non-rotating tile
			{
				translate([0, 0, wall_thickness-size[2]/2])
					cylinder(h=connector_depth, d=magnet_separation-magnet_diameter-wall_thickness, center=false);
			}
			
			//Clear space between tabs
			if(type >= 0)
				translate([0,0,connector_depth/2+DELTA])
					cube([size[1]+MARGIN,size[0]+MARGIN,size[2]-connector_depth], center=true);

			//Mounting holes for other tiles (located precisely halfway in module height and the same distance from each end)
			quad_mirror()
				translate([size[0]/2-size[2]/2+DELTA, size[1]/2+DELTA, 0])
					rotate([-90, 0, 0])
						translate([0,0,-wall_thickness/2])
							nutmount(containerHeight=wall_thickness, boltDiameter=screw_diameter_chassis, flushTop=false);
		}

	}
}

module quad_mirror(p1=[1,0,0], p2=[0,1,0])
{
    children();
    mirror(p1) children();
    mirror(p2) children();
    mirror(p2) mirror(p1) children();
}

module dual_mirror(p1=[1,0,0])
{
    children();
    mirror(p1) children();
}

module cubeModAssemble(types=[80,50,40,30,10,20], location=[0, 0, 0], size=100)
{
	
	rotate([0,-90,0])
	translate(location)
	{
		rotate([0, 0, 0])
			translate([0, 0, -size/2])
				color([1, 0, 0])
					cubetile(types[0]); //-z
		rotate([180, 0, 0])
			translate([0, 0, -size/2])
				color([0, 1, 0])
					cubetile(types[1]); //+z
		rotate([90, 0, 90])
			translate([0, 0, -size/2])
				color([1, 1, 0])
					cubetile(types[2]); //-x
		rotate([-90, 0, 90])
			translate([0, 0, -size/2])
				color([0, 0, 1])
					cubetile(types[3]); //+x
			rotate([0, 90, 90])
			translate([0, 0, -size/2])
				color([1, 0, 1])
					cubetile(types[4]); //-y
		rotate([0, 90, -90])
			translate([0, 0, -size/2])
				color([0, 1, 1])
					cubetile(types[5]); //+y
	}
}

module cubemodhull(size=CUBE_TILE_SIZE, wall_thickness=WALL_THICKNESS)
{
	cube(size=[size[0]+2*MARGIN,size[0]+2*wall_thickness+2*MARGIN,size[1]+2*MARGIN], center=true);
	cube(size=[size[0]+2*MARGIN,size[1]+2*wall_thickness+2*MARGIN,size[0]+2*MARGIN], center=true);
	cube(size=[size[1]+2*MARGIN,size[0]+2*wall_thickness+2*MARGIN,size[0]+2*MARGIN], center=true);
}

//cubeModAssemble();

//cubetile(90);

catalog = {'VIMS' : ['vCloud Director','OpenStack'],
	    'Orchestrators' : { 'vCloud Director' : ['OSM 3.0','Cloudify 3.4','Cloudify 4.0','RIFT.ware 5.3','TOSCA'],
			       'OpenStack' : ['OSM 3.0','Cloudify 3.4','Cloudify 4.0','RIFT.ware 5.3','TOSCA','Heat']
			      },

            'VNF Types' : {
		             'vCloud Director:OSM 3.0'         : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
		             'vCloud Director:Cloudify 3.4'    : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
			     'vCloud Director:Cloudify 4.0'    : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
			     'vCloud Director:TOSCA'           : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
		             'OpenStack:OSM 3.0'	       : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
	                     'OpenStack:Cloudify 3.4'	       : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
			     'OpenStack:Cloudify 4.0'          : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others'],
			     'OpenStack:RIFT.ware 5.3'         : ['vRouter','Firewall','LoadBalancer','Qos','vEPC','vMS','Others']


             },

            'InputHeads' : { 'vCloud Director:OSM 3.0' : ['VNF Parameters','NIC Parameters','EPA Parameters','Upload Scripts'] } ,


            'VNF Parameters' : { 'vCloud Director:OSM 3.0' :[ 
							['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
							['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
							['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'], 
							['vnf_description', 'optional', 'string that describes VNF in short'],
 							['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
							['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
 							['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
							['disk','mandatory','Disk Storage. Minimum value : 10 GB']

							],
				  'vCloud Director:Cloudify 3.4' : [
						        ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
						        ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
							['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
							['vnf_description', 'optional', 'string that describes VNF in short'],
							['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
							['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
							['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
							['disk','mandatory','Disk Storage. Minimum value : 10 GB']			 
					 	],

				  'vCloud Director:Cloudify 4.0' : [
				                        ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
				                        ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],              
				                        ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
				                        ['vnf_description', 'optional', 'string that describes VNF in short'],
				                        ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],          
				                        ['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
				                        ['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
				                        ['disk','mandatory','Disk Storage. Minimum value : 10 GB']
			             ], 

                                   'vCloud Director:TOSCA' : [
                                                        ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
                                                        ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
                                                        ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
                                                        ['vnf_description', 'optional', 'string that describes VNF in short'],
                                                        ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
                                                        ['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
                                                        ['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
                                                        ['disk','mandatory','Disk Storage. Minimum value : 10 GB']
                                     ],

                                
                                  'OpenStack:OSM 3.0' : [
					       ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
					       ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
					       ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
					       ['vnf_description', 'optional', 'string that describes VNF in short'],
					       ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
					       ['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
					       ['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
					       ['disk','mandatory','Disk Storage. Minimum value : 10 GB']			
                                          ],

				   'OpenStack:Cloudify 3.4' : [ 
					      ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
					      ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
					      ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
					      ['vnf_description', 'optional', 'string that describes VNF in short'],
					      ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],	
			                      ['Flavor','mandatory','Allowed Values m1.small,m1.medium,m1.large,Custom'],
					      ['cpu','mandatory', 'cpu param value should be provided only when flavor = Custom.Allowed values 1,2,4,8,16'],
					      ['ram','mandatory', 'ram param value should be provided only when flavor = Custom.Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
		                              ['disk','mandatory','disk param value should be provided only when flavor = Custom.Disk Storage. Minimum value : 10 GB']
],

                                  'OpenStack:Cloudify 4.0' : [
                                              ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
                                              ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
                                              ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
                                              ['vnf_description', 'optional', 'string that describes VNF in short'],
                                              ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
                                              ['Flavor','mandatory','Allowed Values m1.small,m1.medium,m1.large,Custom'],
                                              ['cpu','mandatory', 'cpu param value should be provided only when flavor = Custom.Allowed values 1,2,4,8,16'],
                                              ['ram','mandatory', 'ram param value should be provided only when flavor = Custom.Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
                                              ['disk','mandatory','disk param value should be provided only when flavor = Custom.Disk Storage. Minimum value : 1 0 GB'] 
],


                                  'OpenStack:TOSCA' : [
                                              ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
                                              ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
                                              ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
                                              ['vnf_description', 'optional', 'string that describes VNF in short'],
                                              ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
                                              ['Flavor','mandatory','Allowed Values m1.small,m1.medium,m1.large,Custom'],
                                              ['cpu','mandatory', 'cpu param value should be provided only when flavor = Custom.Allowed values 1,2,4,8,16'],
                                              ['ram','mandatory', 'ram param value should be provided only when flavor = Custom.Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
                                              ['disk','mandatory','disk param value should be provided only when flavor = Custom.Disk Storage. Minimum value : 1 0 GB']
],
				 
				 'OpenStack:RIFT.ware 5.3' : [
         				    ['env_type','mandatory','VIM type: vCloud Director/OpenStack for which to generate a blueprint'],
			                    ['vnf_type','mandatory','VNF type: VNF type for which blueprint to generate a blueprint'],
				            ['vnf_name', 'mandatory', 'User provided vnf name. Should be string  with no spaces'],
			                    ['vnf_description', 'optional', 'string that describes VNF in short'],
			                    ['image_id','mandatory','Unique Identifier of the existing vnf image in target environment' ],
				            ['cpu','mandatory', 'Allowed values 1,2,4,8,16'],
			                    ['ram','mandatory', 'Main Memory in MB. Allowed values: 1024,2048,4096,8192,16384,32768,65536,131072'],
			                    ['disk','mandatory','Disk Storage. Minimum value : 10 GB']
        ],
	
	         
							       	

		
       },
	
	  'NIC Parameters' : { 'vCloud Director:OSM 3.0' : [['nic{}_name', 'mandatory', 'Network Interface Name. Max 6 NICs supported. NIC no to be mentioned at {}' ],
						            ['Interfaces{}_name','mandatory', 'Allowed Values E1000,VNXNET3']		
                                                           ],

				'vCloud Director:Cloudify 3.4' : [ 
                      					['nic{}_name', 'mandatory', 'Network Name. This should be the network that exists in VIM. Max 6 NICs supported. NIC no to be mentioned at {}' ],
                                                        ['Interfaces{}_name','mandatory', 'Allowed Values Default']
					],

                                'vCloud Director:Cloudify 4.0' : [
                                                        ['nic{}_name', 'mandatory', 'Network Name. This should be the Network that exists in VIM. Max 6 NICs supported. NIC no to be mentioned at {}' ],
                                                        ['Interfaces{}_name','mandatory', 'Allowed Values Default']
				],

				'vCloud Director:TOSCA' : [['nic{}_name', 'mandatory', 'Network Interface Name. Max 6 NICs supported. NIC no to be mentioned at {}' ],
                                                            ['Interfaces{}_name','mandatory', 'Allowed Values E1000,VNXNET3']
                                                           ],



                                'OpenStack:TOSCA' : [
                                                        ['nic{}_name', 'mandatory', 'Network Interface Name. Max 6 NICs supported. NIC no to be mentioned at {}' ],
                                                        ['Interfaces{}_name','mandatory', 'Allowed Values VIRTIO,PCI-PASSTHROUGH,SR-IOV,E1000,VMXNET3']
             ],
			       'OpenStack:OSM 3.0' : [
						 	['nic{}_name', 'mandatory', 'Network Interface Name. Max 6 NICs supported. NIC no to be mentioned at {}' ],
							['Interfaces{}_name','mandatory', 'Allowed Values VIRTIO,PCI-PASSTHROUGH,SR-IOV,E1000,VMXNET3']
						     ],		


			        'OpenStack:RIFT.ware 5.3' : [
				                              ['nic{}_name', 'mandatory', 'Network Interface Name. Max 6 NICs supported. NIC no to be mentioned at {}'],

					                      ['Interfaces{}_name','mandatory', 'Allowed Values VIRTIO,PCI-PASSTHROUGH,SR-IOV,E1000,VMXNET3']
                      ]
                             },

          'EPA Parameters' : { 'vCloud Director:OSM 3.0' : [ 
							   ['memory_reservation','optional', 'Allowed values True or False'],
							   ['latency_sensitivity','optional', 'Allowed values True of False'],
					                   ['numa_affinity','optional', 'Allowed values True or False'],
							   ['number_numa_node','optional', 'To be set only if numa_affinity is set']	


							   ],

                              'vCloud Director:TOSCA' : [
                                                           ['memory_reservation','optional', 'Allowed values True or False'],
                                                           ['latency_sensitivity','optional', 'Allowed values True of False'],
                                                           ['numa_affinity','optional', 'Allowed values True or False'],
                                                           ['number_numa_node','optional', 'To be set only if numa_affinity is set']


                                                           ],


			     'vCloud Director:Cloudify 3.4' : [ 'EPA Parameters not supported for vCloud Director + Cloudify 3.4 combination'],

			     'vCloud Director:Cloudify 4.0' : [ 'EPA Parameters not supported for vCloud Director + Cloudify 4.0 combination'] ,
  	
			      'OpenStack:OSM 3.0' : 	[
								['memory_reservation','optional', 'Allowed values True or False'],
								['latency_sensitivity','optional', 'Allowed values True or False'],
								['numa_affinity','optional', 'Allowed values True or False'],
								['number_numa_node','optional', 'To be set only if numa_affinity is set']	
							] ,

			       'OpenStack:TOSCA' :     [
                                                                ['memory_reservation','optional', 'Allowed values True or False'],
                                                                ['latency_sensitivity','optional', 'Allowed values True or False'],
                                                                ['numa_affinity','optional', 'Allowed values True or False'],
                                                                ['number_numa_node','optional', 'To be set only if numa_affinity is set']   
                                                        ] ,


                               'OpenStack:Cloudify 3.4' :  [  

								['memory_reservation','optional','Supported only for Custom flavor. Allowed values True or False'],
								['latency_sensitivity','optional', 'Supported only for Custom flavor.Allowed values True or False'],
								['numa_affinity','optional','Supported only for Custom flavor.Allowed values True or False'],
								['number_numa_node','optional', 'Supported only for Custom flavor.To be set only if numa_affinity is set']  
				],
			    



                                'OpenStack:Cloudify 4.0' :  [

                                                                ['memory_reservation','optional','Supported only for Custom flavor. Allowed values True or False'],
                                                                ['latency_sensitivity','optional', 'Supported only for Custom flavor.Allowed values True or False'],
                                                                ['numa_affinity','optional','Supported only for Custom flavor.Allowed values True or False'],
                                                                ['number_numa_node','optional', 'Supported only for Custom flavor.To be set only if numa_affinity is set'] 
				],

			        'OpenStack:RIFT.ware 5.3' : [

				                                  ['memory_reservation','optional', 'Allowed values True or False'],
       					                          ['latency_sensitivity','optional', 'Allowed values True or False'],
				                                  ['numa_affinity','optional', 'Allowed values True or False'],
                               					  ['number_numa_node','optional', 'To be set only if numa_affinity is set']
                          				    ],

				},


           'Upload Scripts': { 'vCloud Director:OSM 3.0' : [ 'cloud_init_script','optional','Initialization script. Input type : File'],
			       'vCloud Director:Cloudify 3.4' : [ [ 'create','optional','Initialization script. Input type : File'],	
								  [ 'config','optinal','Configuration script. Input type : File'],
								  [ 'delete','optional','Deletion script. Input type : File']
								],


				'vCloud Director:Cloudify 4.0' : [ [ 'create','optional','Initialization script. Input type : File'],
                                                                   [ 'config','optinal','Configuration script. Input type : File'],
                                                                   [ 'delete','optional','Deletion script. Input type : File']
                                                                ],
                                
				'vCloud Director:TOSCA' : [ [ 'create','optional','Initialization script. Input type : File'],
                                   			    [ 'config','optional','Configuration script. Input type : File'],
                                   			    [ 'delete','optional','Deletion script. Input type : File']
                                                          ],


				'OpenStack:TOSCA' : [ 
								[ 'create','optional','Initialization script. Input type : File'],
				                                [ 'config','optional','Configuration script. Input type : File'],
					                        [ 'delete','optional','Deletion script. Input type : File']
                          				  ],

                                
         		         'OpenStack:OSM 3.0' : ['cloud_init_script','optional','Initialization script. Input type : File'],

				 'OpenStack:Cloudify 3.4' : [
				                                [ 'create','optional','Initialization script. Input type : File'],
                               				        [ 'config','optional','Configuration script. Input type : File'],
				                                [ 'delete','optional','Deletion script. Input type : File']
                          				    ],

				 'OpenStack:Cloudify 4.0' : [        [ 'create','optional','Initialization script. Input type : File'],
                                 				     [ 'config','optinal','Configuration script. Input type : File'],
				                                     [ 'delete','optional','Deletion script. Input type : File']
                                			    ],

				 'OpenStack:RIFT.ware 5.3' : ['cloud_init_script','optional','Initialization script. Input type : File']
								  
                             }

                              
           }	
def _getVIMs():
  return catalog['VIMS']

def _getOrchsforVIM(vim):
   print "_getOrchs:" ,catalog['Orchestrators'][vim]
   return catalog['Orchestrators'][vim]

def _getVNFTypes(vim,orch):
    return catalog['VNF Types'][vim + ':' + orch]

def _getInputHeads(vim,orch):
   print "_getInputHeads",catalog['InputHeads'][vim + ':' + orch]
   return catalog['InputHeads'][vim + ':' + orch]

def _getInputHeadDetails(vim,orch,inputHead):
    print " _getInputHeadDetails :",vim,orch,inputHead
    return catalog[inputHead][vim + ':' + orch]


if __name__ == '__main__':
   print _getInputHeadDetails('vCloud Director', 'OSM 3.0','VNF Parameters')


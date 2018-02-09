/**
 * Created by jakub on 1/19/17.
 */
const TOOLTIPS = require('../config/tooltips.json');

module.exports = {
  template: require('../templates/epa_configuration_ost_osm.html'),
  controller: function ( dataService, $scope) {
    "ngInject";
	
	this.FORM_SUBMIT_CLASS = 'submit';
    this.NO_CLASS = '';
	this.DISABLED_FORM_GROUP = 'form-group disabled';
    this.FORM_GROUP = 'form-group';
	this.INPUT_PLACEHOLDER = "select number of numa node";
	this.NUMBER_NUMA_NODE ;
	this.NUMA_AFFINITY = false;
	this.MEMORY_RESERVATION = false;
	this.LATENCY_SENSITIVITY = false;
	
	$scope.NumaAffinitySelected = false;
	$scope.MemoryReservationSelected = false;
	$scope.LatencySensitivitySelected = false;
	$scope.NumberNumaNodeSelected ;
	
	$scope.SRIOVInterfacesSelected = [];
	
	const config_vnf = dataService.getVnfDefinition();
	this.VIMType = config_vnf.VIMType;
	this.OrchType = config_vnf.OrchType;
	
	
	const config_nic = dataService.getNicDefintion();
	$scope.NICs = remove_dups(config_nic.NICs);
	
	
	
	

	/*$scope.$watch('SRIOVInterfacesSelected',function(newValue,oldValue){
		console.log('Old - '+oldValue+' New -' + newValue );
		
	});*/
	
		
   function  remove_dups(object){	   
		var NICs = [];
		for (i = 0; i < object.length ; i++) {
				if (typeof object[i] !== 'undefined' && object[i] !== null && object[i] != ""){	
				NICs.push(object[i]);
			}
		}
		return NICs;
	}
	
	dataService.setSubmitCallback( function () {
		
		this.formSubmit = true;
		var isValid = this.forms.epaDefinitionForm.$valid;
		
		if( isValid ) {
			var config = {
			  NumaAffinity: $scope.NumaAffinitySelected,
			  MemoryReservation: $scope.MemoryReservationSelected,
			  LatencySensitivity: $scope.LatencySensitivitySelected,
			  NumberNumaNode:$scope.NumberNumaNodeSelected,
			  SRIOVInterfaces:$scope.SRIOVInterfacesSelected
					  
			};
			dataService.setEPA( config);
			//console.log(config);
		}
		return isValid;
		
	}.bind(this));
  }
};

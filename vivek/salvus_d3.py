import uuid

class d3_line_graph:
    def __init__(self, data, salvus):
    	self.graph_id = 'graph-'+str(uuid.uuid4())
        self.data = data
    	salvus.html("""<div id=%s class="aGraph" style="position:relative;top:0px;left:0px; float:left;"></div>""" % self.graph_id)
    	salvus.javascript("""
            var m = [20, 40, 40, 60]; // margins
            var w = 1000 - m[1] - m[3]; // width
            var h = 400 - m[0] - m[2]; // height
            
            data = obj
            
            var x_values = []
            for (var i=0; i<data.length; i++) {{ x_values[i] = data[i].x }}
            
            var y_values = []
            for (var i=0; i<data.length; i++) {{ y_values[i] = data[i].y }}
            
            //var x_values = obj.x
            //var y_values = obj.y
            
            //var data = []
            //for (var i=0; i<x_values.length; i++) {{data[i] = {{x:x_values[i], y:y_values[i]}} }}
                        
            var scale_x = d3.scale.linear().domain([d3.min(x_values), d3.max(x_values)]).range([0, w])
            var scale_y = d3.scale.linear().domain([d3.min(y_values), d3.max(y_values)]).range([h, 0])
            
            var line = d3.svg.line()
                .x(function(d) {{ return scale_x(d.x) }})
                .y(function(d) {{ return scale_y(d.y) }})
             
            var graph = d3.select("#{graph_id}").append("svg:svg")
                            .attr("width", w + m[1] + m[3])
                            .attr("height", h + m[0] + m[2])
                            .append("svg:g")
                            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");
             
            var xAxis = d3.svg.axis().scale(scale_x);
            graph.append("svg:g")
                            .attr("class", "x axis")
                            .attr("transform", "translate(0," + h + ")")
                            .call(xAxis);
             
            var yAxisLeft = d3.svg.axis().scale(scale_y).orient("left");
            
            graph.append("svg:g")
                            .attr("class", "y axis")
                            .attr("transform", "translate(0,0)")
                            .call(yAxisLeft);
            
            
            graph.append("svg:path")
                            .attr("d", line(data))
                            .attr("id","data_line")
			$('#{graph_id}').data('line_function',line)
			""".format(graph_id=self.graph_id), obj=self.data)

        
    def update_graph(self, salvus):
		salvus.javascript("""
			var x_values = obj.x
            var y_values = obj.y
            
            var data = []
            for (var i=0; i<x_values.length; i++) {{data[i] = {{x:x_values[i], y:y_values[i]}} }}            
            
            line = $('#{graph_id}').data('line_function')
            d3.select("#{graph_id}").select("#data_line").attr("d",line(data))
			""".format(graph_id=self.graph_id), 
		obj=self.data)
        
    
def make_cached_slider(lookup_list, line_graph, salvus):
    """
    lookup_table should be a list of objects with the same type as line_graph.data 
    corresponding to the values of data for each slider position
    
    line_graph should be a salvus_d3.d3_line_graph object
    """
    
    slider_css_id = uuid.uuid4()
    
    salvus.html("""<div id="wrapper-{css_id}" style="width:1000px;height:40px">
    					<div id="{css_id}" style="top:15px;left:30px"></div>	
                   </div>""".format(css_id=slider_css_id))
    
    salvus.javascript("""
                	line = $('#{graph_id}').data('line_function')
					data_list = obj
                    
                    $("#{slider_id}").slider({{ min:1, max:data_list.length, step:1 }});
                    
                    $("#{slider_id}").on( "slide", function( event, ui ) {{
						            var current_data = data_list[ui.value];
						  			//d3.select("#{graph_id}").select("#data_line").transition().duration(1000).attr("d",line(current_data))
                                    d3.select("#{graph_id}").select("#data_line").attr("d",line(current_data))
                                          }} )
                     """.format(slider_id = slider_css_id, 
                                graph_id  = line_graph.graph_id),
                      obj=lookup_list)


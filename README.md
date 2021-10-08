# mini_mes
Resilience mini-mes

Your goal is to implement a backend system that simulates aspects of the system in biopharmaceutical manufacturing called the Manufacturing Execution System (MES), which sits atop the procedures involved in the manufacturing process.

Traditionally, biopharmaceutical products (medicines, therapies, vaccines, etc.) are produced by manufacturing systems in batches. For a given product, there is a defined process for making the batches involving various types of systems such as bioreactors, scales, drying machines, water purification, etc. 

These processes are precisely developed with safety and quality of utmost concern. If a function is not executed correctly or an anomaly occurs undetected during the production of a batch, the efficacy or safety of the resulting product is compromised. 

In biopharmaceutical production, products have specified Critical Quality Attributes (CQA) that define the qualities a product must have to fit its purpose and safety. To support these, the processes have Critical Process Parameters (CPP) that define the bounds within which the process must remain to produce a successful batch (a product that is both safe and effective). 

In some cases, an MES interacts directly with the manufacturing systems, such as a bioreactor, to monitor and directly control the steps of the process. You will implement a simple "mini-MES" automation server that uses a REST API to access devices to execute a process. You can use whatever language/framework/runtime you are comfortable with for this implementation. 

The process to be executed involves a simplified version of a bioreactor, which is a device that takes biologically active ingredients in a vessel so they can interact in a controlled way. 

The simplified process to be executed consists of the following steps:  

Open the fill valve to allow material in. 
Let the vessel fill to (70 +/-2)% full. 
If the pressure of the vessel reaches 200 kPa the batch should be aborted by opening the output valve, so the material is let out and the process is stopped. 
When the temperature of the container reaches (80 +/-1) degrees Celsius, open the output valve to let the material out. 

Once the vessel is emptied, this fictional batch will be considered done. 

As important as the product of the batch itself is the "Batch Record," which reports the activity for the batch. After completion of the batch your mini-MES should report a Batch Record that provides the following information: 

Whether the batch was considered successful 
Actual fill level reached in the vessel 
Temperature range during the process 
pH range during the process 
Pressure range during the process 
Total time for the process 
Whether the CPP of +/- 2% for vessel fill level was met 
Whether the CPP of +/- 1 degree Celsius for maximum temperature was met 
Whether the CPP of pressure held below 200 kPa was met 

REST API Specification: 

bioreactor/0 

             GET 

Used to get a bioreactor for use. Returns the <id> of the bioreactor to use. 

bioreactor/`<id>`
           
            GET 

Returns the current readings for the interior of the vessel of the bioreactor. 

Fill-level – Percentage 
pH 
Pressure – kPa 
Temperature – degrees Celsius 
 
bioreactor/`<id>`/input-valve
  
            GET 
Whether the state of the input valve is open or closed. 
  
            PUT 
Used to set the state of the input valve to open or closed. 

bioreactor/`<id>`/output-valve 
  
            GET 

Whether the state of the output valve is open or closed. 
            
            PUT 

Used to set the state an output valve to open or closed. 

import {
  Plus,
  Trash2,
  Edit,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import client from "../api/client";

import Layout from "../components/Layout";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";



const EMPTY_FORM = {

  email:"",
  password:"",

  first_name:"",
  last_name:"",

  phone:"",

  photo:null,

  emergency_contact_name:"",
  emergency_contact_phone:"",

  address:"",

  identification_type:"CITIZENSHIP",
  identification_number:"",

  identification_document_front:null,
  identification_document_back:null,

  university:"",
  student_id:"",
  course:"",

};




const FIELD_LABELS = {

  email:"Email",
  password:"Password",

  first_name:"First Name",
  last_name:"Last Name",

  phone:"Phone",

  photo:"Photo",

  emergency_contact_name:
  "Emergency Contact Name",

  emergency_contact_phone:
  "Emergency Contact Phone",

  address:"Address",

  identification_type:
  "Identification Type",

  identification_number:
  "Identification Number",

  identification_document_front:
  "Identification Document Front",

  identification_document_back:
  "Identification Document Back",

  university:"University",

  student_id:"Student ID",

  course:"Course",

};




function formatError(err){

  if(err?.response?.data){

    return Object.entries(
      err.response.data
    )
    .map(
      ([key,value]) =>
      `${key}: ${
        Array.isArray(value)
        ? value.join(", ")
        : value
      }`
    )
    .join("\n");

  }


  return "Something went wrong";

}






export default function TenantsPage(){


const [tenants,setTenants] = useState([]);

const [beds,setBeds] = useState([]);


const [loading,setLoading] = useState(true);


const [error,setError] = useState("");



const [addDrawer,setAddDrawer] = useState(false);

const [editDrawer,setEditDrawer] = useState(false);

const [assignDrawer,setAssignDrawer] = useState(false);



const [editingTenant,setEditingTenant] = useState(null);


const [selectedTenant,setSelectedTenant] = useState(null);


const [selectedBed,setSelectedBed] = useState("");



const [checkIn,setCheckIn] = useState(
  new Date()
  .toISOString()
  .slice(0,10)
);



const [form,setForm] = useState({
  ...EMPTY_FORM
});







async function load(){


try{


const [
  tenantsRes,
  bedsRes
] = await Promise.all([


  client.get("/tenant-profiles/"),


  client.get("/beds/")


]);





setTenants(

  tenantsRes.data.results ??
  tenantsRes.data

);






// ONLY SHOW REAL VACANT BEDS

setBeds(

  (bedsRes.data.results ??
  bedsRes.data)

  .filter(
    bed =>
    bed.status === "VACANT"
  )

);



}

catch(err){


console.log(err);


setError(
  "Unable to load tenants"
);


}


finally{


setLoading(false);


}


}






useEffect(()=>{

  load();

},[]);








function handleChange(e){


setForm({

  ...form,

  [e.target.name]:
  e.target.value

});


}







function handleFileChange(e){


setForm({

  ...form,

  [e.target.name]:
  e.target.files[0]

});


}







function resetForm(){

setForm({
  ...EMPTY_FORM
});

}






function closeAdd(){


setAddDrawer(false);

resetForm();

setError("");

}




function closeEdit(){


setEditDrawer(false);

setEditingTenant(null);

resetForm();

setError("");

}





function openAssign(tenant){


setError("");

setSelectedTenant(tenant);

setSelectedBed("");

setAssignDrawer(true);


}





async function refresh(){

await load();

}




async function createTenant(){


try{


const data = new FormData();



Object.keys(form).forEach(key=>{


if(
  form[key] !== null &&
  form[key] !== ""
){

  data.append(
    key,
    form[key]
  );

}


});




await client.post(

"/tenant-profiles/",

data,

{

headers:{
"Content-Type":
"multipart/form-data"
}

}

);



closeAdd();


await refresh();



}

catch(err){


console.log(err);


setError(
formatError(err)
);


}


}







function openEdit(tenant){


setError("");


setEditingTenant(tenant);



setForm({

email:
tenant.user_detail?.email || "",


password:"",


first_name:
tenant.user_detail?.first_name || "",


last_name:
tenant.user_detail?.last_name || "",


phone:
tenant.user_detail?.phone || "",


photo:null,


emergency_contact_name:
tenant.emergency_contact_name || "",


emergency_contact_phone:
tenant.emergency_contact_phone || "",


address:
tenant.address || "",


identification_type:
tenant.identification_type || "CITIZENSHIP",


identification_number:
tenant.identification_number || "",


identification_document_front:null,


identification_document_back:null,


university:
tenant.university || "",


student_id:
tenant.student_id || "",


course:
tenant.course || "",


});


setEditDrawer(true);


}








async function updateTenant(){


try{


const data = new FormData();



Object.keys(form).forEach(key=>{


if(

form[key] !== null &&

form[key] !== "" &&

key !== "password"

){


data.append(
key,
form[key]
);


}


});






await client.patch(

`/tenant-profiles/${editingTenant.id}/`,

data,

{

headers:{

"Content-Type":
"multipart/form-data"

}

}

);



closeEdit();


await refresh();



}

catch(err){


console.log(err);


setError(
formatError(err)
);


}


}








async function assignBed(){


if(!selectedBed)
return;




try{


await client.post(

"/beds/allocations/",

{

bed:selectedBed,

tenant:selectedTenant?.user,

check_in_date:checkIn

}

);




setAssignDrawer(false);


setSelectedTenant(null);


setSelectedBed("");



await refresh();



}

catch(err){


console.log(err);



setError(
formatError(err)
);



await refresh();



}


}







async function checkout(allocationId){



if(
!window.confirm(
"Checkout this tenant?"
)
)

return;




try{


await client.patch(

`/beds/allocations/${allocationId}/`,

{

check_out_date:

new Date()

.toISOString()

.slice(0,10)

}

);




await refresh();



}

catch(err){


setError(
formatError(err)
);


}



}








async function removeTenant(id){



if(
!window.confirm(
"Delete tenant?"
)
)

return;




try{


await client.delete(

`/tenant-profiles/${id}/`

);




await refresh();



}

catch(err){


setError(
formatError(err)
);


}


}








const columns=[



{

key:"name",

header:"Tenant",

render:(row)=>

row.user_detail?.first_name

?

`${row.user_detail.first_name} ${row.user_detail.last_name}`

:

row.user_detail?.email || "-"

},






{

key:"email",

header:"Email",

render:(row)=>

row.user_detail?.email || "-"

},






{

key:"phone",

header:"Phone",

render:(row)=>

row.user_detail?.phone || "-"

},



{

key:"hostel",

header:"Hostel",

render:(row)=>

row.current_allocation?.hostel || "-"

},






{

key:"room",

header:"Room",

render:(row)=>

row.current_allocation?.room_number || "-"

},






{

key:"bed",

header:"Bed",

render:(row)=>

row.current_allocation?.bed_number || "-"

},






{

key:"status",

header:"Status",

render:(row)=>

row.current_allocation

?

"Occupied"

:

"Unassigned"

},






{

key:"actions",

header:"Actions",

render:(row)=>(


<div className="flex gap-2 items-center">



{

row.current_allocation

?

<button

className="
px-3
py-1
bg-red-100
text-red-700
rounded
"

onClick={()=>checkout(
row.current_allocation.allocation_id
)}

>

Checkout

</button>


:

<button

className="
px-3
py-1
bg-green-100
text-green-700
rounded
"

onClick={()=>openAssign(row)}

>

Assign Bed

</button>


}







<button

className="
text-blue-600
hover:text-blue-800
"

onClick={()=>openEdit(row)}

>

<Edit size={16}/>

</button>







<button

className="
text-red-600
hover:text-red-800
"

onClick={()=>removeTenant(row.id)}

>

<Trash2 size={16}/>

</button>




</div>


)


}


];

return (

<Layout>


<div className="space-y-6">



<div className="flex justify-between items-center">


<div>

<h1 className="text-2xl font-bold">
Tenants
</h1>


<p className="text-gray-500">
Manage residents and bed allocation
</p>


</div>





<button

onClick={()=>{

setError("");

resetForm();

setAddDrawer(true);

}}

className="
bg-blue-600
hover:bg-blue-700
text-white
px-4
py-2
rounded-lg
flex
items-center
gap-2
"

>

<Plus size={18}/>

Add Tenant

</button>


</div>







{

error &&

<div className="
bg-red-100
text-red-700
p-3
rounded
whitespace-pre-line
">

{error}

</div>

}







<DataTable

columns={columns}

rows={tenants}

loading={loading}

/>









{/* ADD TENANT */}


<FormDrawer

open={addDrawer}

title="Add Tenant"

onClose={closeAdd}

>


<TenantForm

form={form}

setForm={setForm}

handleChange={handleChange}

handleFileChange={handleFileChange}

onSubmit={createTenant}

buttonText="Create Tenant"

/>


</FormDrawer>









{/* EDIT TENANT */}


<FormDrawer

open={editDrawer}

title="Edit Tenant"

onClose={closeEdit}

>


<TenantForm

form={form}

setForm={setForm}

handleChange={handleChange}

handleFileChange={handleFileChange}

onSubmit={updateTenant}

buttonText="Update Tenant"

editMode

/>




</FormDrawer>









{/* ASSIGN BED */}


<FormDrawer

open={assignDrawer}

title="Assign Bed"

onClose={()=>setAssignDrawer(false)}

>


<div className="space-y-4">


<h3 className="font-semibold">

{
selectedTenant?.user_detail?.first_name
}

{" "}

{
selectedTenant?.user_detail?.last_name
}

</h3>







<select

className="
border
p-2
rounded
w-full
"

value={selectedBed}

onChange={
e=>setSelectedBed(e.target.value)
}

>


<option value="">
Select Vacant Bed
</option>




{

beds.map(b=>(


<option

key={b.id}

value={b.id}

>

Room {b.room_number || b.room}

{" | "}

Bed {b.bed_number}

</option>


))

}


</select>








<input

type="date"

value={checkIn}

onChange={
e=>setCheckIn(e.target.value)
}

className="
border
p-2
rounded
w-full
"

/>








<button

onClick={assignBed}

className="
bg-blue-600
hover:bg-blue-700
text-white
w-full
p-2
rounded-lg
"

>

Assign Bed

</button>




</div>


</FormDrawer>





</div>


</Layout>


);

}





function TenantForm({

form,

handleChange,

handleFileChange,

onSubmit,

buttonText,

editMode=false

}){


return (

<div className="space-y-3">


{

Object.keys(form).map(field=>{


if(
editMode &&
(
field==="email" ||
field==="password"
)

)

return null;







if(field==="identification_type"){


return (

<select

key={field}

name={field}

value={form[field] || ""}

onChange={handleChange}

className="
border
p-2
rounded
w-full
"

>


<option value="">
Select Identification Type
</option>


<option value="CITIZENSHIP">
Citizenship
</option>


<option value="PASSPORT">
Passport
</option>


<option value="NATIONAL_ID">
National ID
</option>



</select>


)


}








if(field==="address"){


return (

<textarea

key={field}

name={field}

placeholder={FIELD_LABELS[field]}

value={form[field] || ""}

onChange={handleChange}

className="
border
p-2
rounded
w-full
"

/>


)


}









if(

field==="photo"

||

field.includes("document")

){


return (

<div key={field}>


<label className="text-sm">

{FIELD_LABELS[field]}

</label>



<input

type="file"

name={field}

onChange={handleFileChange}

className="
border
p-2
rounded
w-full
"

/>


</div>


)


}








return (

<input

key={field}

name={field}

placeholder={FIELD_LABELS[field]}

value={form[field] || ""}

onChange={handleChange}

type={
field==="password"
?
"password"
:
"text"
}

className="
border
p-2
rounded
w-full
"

/>


)


})

}





<button

onClick={onSubmit}

className="
bg-blue-600
hover:bg-blue-700
text-white
w-full
p-2
rounded-lg
"

>

{buttonText}

</button>



</div>


)

}
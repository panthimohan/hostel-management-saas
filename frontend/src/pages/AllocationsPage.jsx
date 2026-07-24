import { useEffect, useState } from "react";
import { Plus } from "lucide-react";

import client from "../api/client";
import Layout from "../components/Layout";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";


const EMPTY_FORM = {
    tenant:"",
    bed:"",
    check_in_date:""
};


export default function AllocationsPage(){

    const [allocations,setAllocations] = useState([]);
    const [tenants,setTenants] = useState([]);
    const [beds,setBeds] = useState([]);

    const [form,setForm] = useState(EMPTY_FORM);

    const [open,setOpen] = useState(false);

    const [loading,setLoading] = useState(true);

    const [error,setError] = useState("");



    async function load(){

        setLoading(true);

        try{

            const [
                allocationRes,
                tenantRes,
                bedRes
            ] = await Promise.all([

                client.get("/beds/allocations/"),

                client.get("/tenant-profiles/"),

                client.get("/beds/?status=VACANT")

            ]);


            setAllocations(
                allocationRes.data.results || allocationRes.data
            );


            setTenants(
                tenantRes.data.results || tenantRes.data
            );


            setBeds(
                bedRes.data.results || bedRes.data
            );


        }catch(err){

            console.log(err);

            setError("Failed loading allocations");

        }
        finally{

            setLoading(false);

        }

    }



    useEffect(()=>{

        load();

    },[]);



    function change(e){

        setForm({

            ...form,

            [e.target.name]:e.target.value

        });

    }



    async function submit(){

        try{

            await client.post(
                "/beds/allocations/",
                form
            );


            setOpen(false);

            setForm(EMPTY_FORM);

            load();


        }catch(err){

            console.log(err);

            setError(
                JSON.stringify(err.response?.data)
            );

        }

    }




    const columns=[

        {
            key:"tenant",
            header:"Tenant",
            render:(row)=>
                row.tenant_email ||
                row.tenant
        },


        {
            key:"bed",
            header:"Bed",
            render:(row)=>
                row.bed
        },


        {
            key:"check_in_date",
            header:"Check In"
        },


        {
            key:"check_out_date",
            header:"Check Out"
        }

    ];




return (

<Layout>

<div className="space-y-6">


<div className="flex justify-between items-center">


<div>

<h1 className="text-2xl font-bold">
Bed Allocation
</h1>

<p className="text-gray-500">
Assign tenants to rooms and beds
</p>

</div>



<button

onClick={()=>setOpen(true)}

className="flex items-center gap-2 bg-black text-white px-4 py-2 rounded-lg"

>

<Plus size={18}/>

Assign Bed

</button>


</div>



{error &&

<div className="bg-red-100 text-red-700 p-3 rounded">

{error}

</div>

}



<DataTable

columns={columns}

rows={allocations}

emptyLabel="No allocations yet."

/>





<FormDrawer

open={open}

title="Assign Tenant Bed"

onClose={()=>setOpen(false)}

>


<div className="space-y-4">



<select

name="tenant"

value={form.tenant}

onChange={change}

className="w-full border p-2 rounded"

>


<option value="">
Select Tenant
</option>


{tenants.map(t=>(

<option

key={t.user}

value={t.user}

>

{t.user_detail?.email}

</option>

))}


</select>





<select

name="bed"

value={form.bed}

onChange={change}

className="w-full border p-2 rounded"

>


<option value="">
Select Bed
</option>


{beds.map(b=>(

<option

key={b.id}

value={b.id}

>

Room {b.room} - Bed {b.bed_number}

</option>

))}


</select>





<input

type="date"

name="check_in_date"

value={form.check_in_date}

onChange={change}

className="w-full border p-2 rounded"

/>




<button

onClick={submit}

className="w-full bg-black text-white py-2 rounded"

>

Assign

</button>



</div>


</FormDrawer>



</div>

</Layout>

);


}
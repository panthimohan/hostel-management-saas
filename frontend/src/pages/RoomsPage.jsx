import { Plus, Pencil, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";

import client from "../api/client";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";
import KeyTag from "../components/KeyTag";
import Layout from "../components/Layout";


const EMPTY_ROOM = {
  id: null,
  hostel: "",
  room_number: "",
  floor: 0,
  capacity: 1,
  room_type: "SINGLE",
  price: ""
};


const EMPTY_BED = {
  id: null,
  room: "",
  bed_number: ""
};



export default function RoomsPage() {


  const [tab,setTab] = useState("rooms");


  const [hostels,setHostels] = useState([]);
  const [rooms,setRooms] = useState([]);
  const [beds,setBeds] = useState([]);


  const [loading,setLoading] = useState(true);


  const [drawerOpen,setDrawerOpen] = useState(false);


  const [roomForm,setRoomForm] = useState(EMPTY_ROOM);
  const [bedForm,setBedForm] = useState(EMPTY_BED);


  const [error,setError] = useState("");

  const [submitting,setSubmitting] = useState(false);





  async function load(){

    setLoading(true);


    try{


      const [
        hostelsRes,
        roomsRes,
        bedsRes

      ] = await Promise.all([

        client.get("/hostels/"),
        client.get("/rooms/"),
        client.get("/beds/")

      ]);



      setHostels(
        hostelsRes.data.results ?? hostelsRes.data
      );


      setRooms(
        roomsRes.data.results ?? roomsRes.data
      );


      setBeds(
        bedsRes.data.results ?? bedsRes.data
      );



    }catch(err){

      console.error(err);

    }
    finally{

      setLoading(false);

    }

  }





  useEffect(()=>{

    load();

  },[]);







  const hostelName=(id)=>{

    return (
      hostels.find(
        h=>h.id===id
      )?.name || "—"
    );

  };






  const roomLabel=(id)=>{


    const room = rooms.find(
      r=>r.id===id
    );


    return room
      ? `Room ${room.room_number}`
      : "—";

  };







  function roomOccupancy(roomId){


    const roomBeds = beds.filter(
      b=>b.room===roomId
    );


    const occupied = roomBeds.filter(
      b=>b.status==="OCCUPIED"
    ).length;


    return {

      occupied,

      vacant:
        Math.max(
          0,
          roomBeds.length - occupied
        )

    };

  }









  function openAdd(){

    setError("");

    if(tab==="rooms"){

      setRoomForm(EMPTY_ROOM);

    }else{

      setBedForm(EMPTY_BED);

    }


    setDrawerOpen(true);

  }







  function editRoom(room){


    setError("");


    setRoomForm({

      id:room.id,

      hostel:room.hostel,

      room_number:room.room_number,

      floor:room.floor,

      capacity:room.capacity,

      room_type:room.room_type,

      price:room.price

    });


    setDrawerOpen(true);


  }








  function editBed(bed){


    setError("");


    setBedForm({

      id:bed.id,

      room:bed.room,

      bed_number:bed.bed_number

    });


    setDrawerOpen(true);


  }










  async function submitRoom(e){

    e.preventDefault();


    setError("");

    setSubmitting(true);



    try{


      if(roomForm.id){


        await client.patch(

          `/rooms/${roomForm.id}/`,

          roomForm

        );


      }else{


        await client.post(

          "/rooms/",

          roomForm

        );


      }



      setDrawerOpen(false);

      setRoomForm(EMPTY_ROOM);


      await load();



    }catch(err){


      const data=err.response?.data;


      setError(

        data

        ? Object.values(data).flat()[0]

        : "Unable to save room"

      );


    }
    finally{

      setSubmitting(false);

    }


  }









  async function submitBed(e){

    e.preventDefault();


    setError("");

    setSubmitting(true);



    try{


      if(bedForm.id){


        await client.patch(

          `/beds/${bedForm.id}/`,

          bedForm

        );


      }else{


        await client.post(

          "/beds/",

          bedForm

        );


      }



      setDrawerOpen(false);

      setBedForm(EMPTY_BED);


      await load();



    }catch(err){


      const data=err.response?.data;


      setError(

        data

        ? Object.values(data).flat()[0]

        : "Unable to save bed"

      );


    }
    finally{

      setSubmitting(false);

    }


  }









  async function deleteRoom(id){


    if(!window.confirm("Delete this room?")) return;



    try{


      await client.delete(

        `/rooms/${id}/`

      );


      await load();


    }catch(err){


      alert(

        err.response?.data?.detail ||

        "Cannot delete room"

      );

    }

  }








  async function deleteBed(id){


    if(!window.confirm("Delete this bed?")) return;



    try{


      await client.delete(

        `/beds/${id}/`

      );


      await load();


    }catch(err){


      alert(

        err.response?.data?.detail ||

        "Cannot delete bed"

      );

    }

  }return (

<Layout>


<div className="flex items-center justify-between mb-6 gap-4 flex-wrap">

<div>

<h1 className="font-display text-2xl font-semibold">
Rooms &amp; Beds
</h1>

<p className="text-sm text-ink-soft mt-1">
Manage rooms, beds and occupancy.
</p>

</div>


<button
onClick={openAdd}
className="btn-primary shrink-0"
>

<Plus size={18}/>

Add {tab==="rooms" ? "room" : "bed"}

</button>


</div>





<div className="flex gap-2 mb-5">


{
["rooms","beds"].map(t=>(

<button

key={t}

onClick={()=>setTab(t)}

className={`px-4 py-2 rounded-full text-sm font-semibold capitalize ${
tab===t
?"bg-primary text-white"
:"bg-surface border border-border text-ink-soft"
}`}

>

{t}

</button>

))
}


</div>





{
loading ? (

<div className="card p-10 text-center">

Loading...

</div>


)

:


tab==="rooms" ? (


<DataTable


emptyLabel="No rooms yet. Add one."


columns={[


{
key:"room_number",
header:"Room Number",
mono:true
},


{
key:"hostel",
header:"Hostel",
render:(r)=>hostelName(r.hostel)
},


{
key:"room_type",
header:"Type"
},


{
key:"capacity",
header:"Capacity",
mono:true
},


{
key:"occupied",
header:"Occupied",

render:(r)=>{

const data=roomOccupancy(r.id);

return `${data.occupied}/${r.capacity}`;

}

},



{
key:"vacant",
header:"Vacant",

render:(r)=>{

const data=roomOccupancy(r.id);

return data.vacant;

}

},



{
key:"price",
header:"Price",

render:(r)=>`$${r.price}`

},



{
key:"status",
header:"Status",

render:(r)=>
<KeyTag status={r.status}/>

},




{
key:"actions",

header:"Actions",

render:(r)=>(

<div className="flex gap-3">


<button

onClick={()=>editRoom(r)}

className="text-primary hover:underline flex items-center gap-1"

>

<Pencil size={15}/>

Edit

</button>



<button

onClick={()=>deleteRoom(r.id)}

className="text-red-600 hover:underline flex items-center gap-1"

>

<Trash2 size={15}/>

Delete

</button>



</div>

)

}


]}


rows={rooms}


/>



)

:

(


<DataTable


emptyLabel="No beds yet. Add one."


columns={[



{
key:"bed_number",
header:"Bed Number",
mono:true
},



{
key:"room",

header:"Room",

render:(r)=>
roomLabel(r.room)

},



{
key:"status",

header:"Status",

render:(r)=>
<KeyTag status={r.status}/>

},




{
key:"actions",

header:"Actions",

render:(r)=>(

<div className="flex gap-3">


<button

onClick={()=>editBed(r)}

className="text-primary hover:underline flex items-center gap-1"

>

<Pencil size={15}/>

Edit

</button>




<button

onClick={()=>deleteBed(r.id)}

className="text-red-600 hover:underline flex items-center gap-1"

>

<Trash2 size={15}/>

Delete

</button>


</div>

)


}



]}


rows={beds}


/>


)


}<FormDrawer

open={drawerOpen}

title={
tab==="rooms"
?
(roomForm.id ? "Edit Room" : "Add Room")
:
(bedForm.id ? "Edit Bed" : "Add Bed")
}

onClose={()=>setDrawerOpen(false)}

>



{
tab==="rooms" ? (


<form

onSubmit={submitRoom}

className="space-y-4"

>



<div>

<label className="label">
Hostel
</label>


<select

required

className="input"

value={roomForm.hostel}

onChange={
e=>
setRoomForm(
f=>({
...f,
hostel:e.target.value
})
)
}

>


<option value="">
Select hostel
</option>


{
hostels.map(h=>(

<option

key={h.id}

value={h.id}

>

{h.name}

</option>

))
}


</select>


</div>







<div className="grid grid-cols-2 gap-3">


<div>

<label className="label">
Room Number
</label>


<input

required

className="input"

value={roomForm.room_number}

onChange={
e=>
setRoomForm(
f=>({
...f,
room_number:e.target.value
})
)
}

/>


</div>





<div>

<label className="label">
Floor
</label>


<input

type="number"

className="input"

value={roomForm.floor}

onChange={
e=>
setRoomForm(
f=>({
...f,
floor:e.target.value
})
)
}

/>


</div>



</div>







<div className="grid grid-cols-2 gap-3">


<div>

<label className="label">
Type
</label>


<select

className="input"

value={roomForm.room_type}

onChange={
e=>
setRoomForm(
f=>({
...f,
room_type:e.target.value
})
)
}

>


<option value="SINGLE">
Single
</option>


<option value="DOUBLE">
Double
</option>


<option value="DORMITORY">
Dormitory
</option>


<option value="SUITE">
Suite
</option>


</select>


</div>






<div>

<label className="label">
Capacity
</label>


<input

type="number"

min="1"

required

className="input"

value={roomForm.capacity}

onChange={
e=>
setRoomForm(
f=>({
...f,
capacity:e.target.value
})
)
}

/>


</div>



</div>







<div>


<label className="label">
Price per bed / month
</label>


<input

type="number"

step="0.01"

required

className="input"

value={roomForm.price}

onChange={
e=>
setRoomForm(
f=>({
...f,
price:e.target.value
})
)
}

/>


</div>







{
error &&

<p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2.5">

{error}

</p>

}







<button

disabled={submitting}

className="btn-primary w-full"

>


{
submitting

?

"Saving..."

:

roomForm.id

?

"Update Room"

:

"Save Room"

}


</button>



</form>




)

:

(



<form

onSubmit={submitBed}

className="space-y-4"

>



<div>

<label className="label">
Room
</label>


<select

required

className="input"

value={bedForm.room}

onChange={
e=>
setBedForm(
f=>({
...f,
room:e.target.value
})
)
}

>


<option value="">
Select room
</option>



{
rooms.map(r=>(


<option

key={r.id}

value={r.id}

>


Room {r.room_number}

{" — "}

{hostelName(r.hostel)}


</option>


))

}


</select>


</div>







<div>

<label className="label">
Bed Number
</label>


<input

required

className="input"

value={bedForm.bed_number}

onChange={
e=>
setBedForm(
f=>({
...f,
bed_number:e.target.value
})
)
}

placeholder="A1"

/>


</div>







{
error &&

<p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2.5">

{error}

</p>

}







<button

disabled={submitting}

className="btn-primary w-full"

>


{
submitting

?

"Saving..."

:

bedForm.id

?

"Update Bed"

:

"Save Bed"

}


</button>



</form>


)

}


</FormDrawer>



</Layout>

);
}
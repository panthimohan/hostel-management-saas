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





export default function RoomsPage(){



const [tab,setTab] = useState("rooms");


const [hostels,setHostels] = useState([]);

const [rooms,setRooms] = useState([]);

const [beds,setBeds] = useState([]);




const [loading,setLoading] = useState(true);


const [drawerOpen,setDrawerOpen] = useState(false);



const [roomForm,setRoomForm] = useState({
  ...EMPTY_ROOM
});


const [bedForm,setBedForm] = useState({
  ...EMPTY_BED
});



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

hostelsRes.data.results ??
hostelsRes.data

);





let roomData =
roomsRes.data.results ??
roomsRes.data;




let bedData =
bedsRes.data.results ??
bedsRes.data;







// sort rooms numerically

roomData.sort(

(a,b)=>

a.room_number.localeCompare(

b.room_number,

undefined,

{
numeric:true
}

)

);







// sort beds room wise

bedData.sort(

(a,b)=>{


if(a.room !== b.room){

return a.room - b.room;

}


return a.bed_number.localeCompare(

b.bed_number,

undefined,

{
numeric:true
}

);


}

);





setRooms(roomData);

setBeds(bedData);




}

catch(err){

console.log(err);

}


finally{

setLoading(false);

}


}








useEffect(()=>{

load();

},[]);









function hostelName(id){


return (

hostels.find(

h=>h.id===id

)?.name ||

"—"

);


}









function roomLabel(id){


const room = rooms.find(

r=>r.id===id

);



return room

?

`Room ${room.room_number}`

:

"—";


}









function roomStats(roomId){


const roomBeds = beds.filter(

b=>b.room===roomId

);



const occupied = roomBeds.filter(

b=>

b.status==="OCCUPIED"

).length;





return {


capacity:

roomBeds.length,


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


setRoomForm({

...EMPTY_ROOM

});


}

else{


setBedForm({

...EMPTY_BED

});


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


setSubmitting(true);

setError("");



try{



if(roomForm.id){


await client.patch(

`/rooms/${roomForm.id}/`,

roomForm

);


}

else{


await client.post(

"/rooms/",

roomForm

);


}





setDrawerOpen(false);



setRoomForm({

...EMPTY_ROOM

});



await load();



}

catch(err){


const data = err.response?.data;



setError(

data

?

Object.values(data).flat()[0]

:

"Unable to save room"

);


}


finally{


setSubmitting(false);


}


}









async function submitBed(e){


e.preventDefault();


setSubmitting(true);

setError("");



try{



if(bedForm.id){


await client.patch(

`/beds/${bedForm.id}/`,

bedForm

);


}

else{


await client.post(

"/beds/",

bedForm

);


}





setDrawerOpen(false);



setBedForm({

...EMPTY_BED

});



await load();



}

catch(err){


const data = err.response?.data;



setError(

data

?

Object.values(data).flat()[0]

:

"Unable to save bed"

);


}


finally{


setSubmitting(false);


}


}
return (

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

className={`
px-4 py-2 rounded-full text-sm font-semibold capitalize

${
tab===t

?

"bg-primary text-white"

:

"bg-surface border border-border text-ink-soft"

}

`}

>

{t}

</button>


))

}


</div>









{
loading ?


<div className="card p-10 text-center">

Loading...

</div>



:




tab==="rooms"

?





<DataTable


emptyLabel="No rooms available."



rows={rooms}



columns={[



{
key:"room_number",

header:"Room",

mono:true

},





{
key:"hostel",

header:"Hostel",

render:(room)=>

hostelName(room.hostel)

},





{
key:"room_type",

header:"Type"

},





{
key:"capacity",

header:"Capacity",

render:(room)=>

room.capacity

},





{
key:"vacant",

header:"Available Beds",

render:(room)=>{


const stats =
roomStats(room.id);



return stats.vacant;


}

},





{
key:"price",

header:"Monthly Rent",

render:(room)=>

`Rs ${room.price}`

},





{
key:"actions",

header:"Actions",


render:(room)=>(


<div className="flex gap-3">





<button

onClick={()=>editRoom(room)}

className="text-primary flex items-center gap-1"

>

<Pencil size={15}/>

Edit

</button>







<button

onClick={()=>deleteRoom(room.id)}

className="text-red-600 flex items-center gap-1"

>

<Trash2 size={15}/>

Delete

</button>





</div>


)


}



]}


/>







:





<div className="space-y-5">


{


rooms.length===0 &&


<div className="card p-8 text-center text-ink-soft">

No rooms created yet.

</div>



}






{


rooms.map(room=>{


const roomBeds = beds.filter(

b=>b.room===room.id

);



return (



<div

key={room.id}

className="card overflow-hidden"

>





<div

className="
px-5
py-4
bg-surface
border-b
border-border
flex
justify-between
items-center
"


>


<div>


<h2 className="font-semibold">

Room {room.room_number}

</h2>



<p className="text-sm text-ink-soft">

{hostelName(room.hostel)}

{" • "}

{room.room_type}

</p>



</div>





<div className="text-sm text-ink-soft">

{roomBeds.length}

Beds

</div>




</div>









<table className="w-full text-sm">


<thead>


<tr className="border-b border-border">


<th className="text-left p-4">

Bed

</th>


<th className="text-left p-4">

Status

</th>


<th className="text-left p-4">

Actions

</th>


</tr>


</thead>







<tbody>



{


roomBeds.length===0

?

<tr>

<td

colSpan="3"

className="p-5 text-center text-ink-soft"

>

No beds added.

</td>

</tr>


:






roomBeds.map(bed=>(


<tr

key={bed.id}

className="border-b border-border"

>


<td className="p-4 font-medium">

{bed.bed_number}

</td>





<td className="p-4">

<KeyTag status={bed.status}/>

</td>





<td className="p-4">


<div className="flex gap-3">





<button

onClick={()=>editBed(bed)}

className="text-primary flex items-center gap-1"

>


<Pencil size={15}/>


Edit


</button>







<button

onClick={()=>deleteBed(bed.id)}

className="text-red-600 flex items-center gap-1"

>


<Trash2 size={15}/>


Delete


</button>





</div>



</td>



</tr>


))


}





</tbody>




</table>





</div>


)


})


}



</div>




}
<FormDrawer

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

tab==="rooms"

?




<form

onSubmit={submitRoom}

className="space-y-4"

>



<div>

<label className="label">

Hostel

</label>


<select

className="input"

required

value={roomForm.hostel}

onChange={e=>

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








<div>

<label className="label">

Room Number

</label>


<input

className="input"

required

placeholder="101A"

value={roomForm.room_number}

onChange={e=>

setRoomForm(

f=>({

...f,

room_number:e.target.value

})

)

}


/>


</div>








<div className="grid grid-cols-2 gap-3">


<div>

<label className="label">

Room Type

</label>



<select

className="input"

value={roomForm.room_type}

onChange={e=>

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

className="input"

value={roomForm.capacity}

onChange={e=>

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

Monthly Rent

</label>


<input

type="number"

className="input"

required

value={roomForm.price}

onChange={e=>

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


<p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2">

{error}

</p>


}









<button

className="btn-primary w-full"

disabled={submitting}

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





:







<form

onSubmit={submitBed}

className="space-y-4"

>




<div>


<label className="label">

Room

</label>



<select

className="input"

required

value={bedForm.room}

onChange={e=>

setBedForm(

f=>({

...f,

room:e.target.value

})

)

}

>


<option value="">

Select Room

</option>




{

rooms.map(room=>(


<option

key={room.id}

value={room.id}

>


Room {room.room_number}

{" - "}

{hostelName(room.hostel)}



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

className="input"

required

placeholder="A1"

value={bedForm.bed_number}

onChange={e=>

setBedForm(

f=>({

...f,

bed_number:e.target.value

})

)

}


/>


</div>








{

error &&


<p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2">

{error}

</p>


}









<button

className="btn-primary w-full"

disabled={submitting}

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





}



</FormDrawer>



</Layout>

);

}
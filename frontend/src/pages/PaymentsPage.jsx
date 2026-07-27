import {
    useEffect,
    useState
} from "react";


import {
    CreditCard,
    Download
} from "lucide-react";


import Layout from "../components/Layout";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";
import StatCard from "../components/StatCard";

import PaymentQRManager from "../components/PaymentQRManager";
import TenantPaymentSubmission from "../components/TenantPaymentSubmission";
import PaymentApproval from "../components/PaymentApproval";

import client from "../api/client";
import { useAuth } from "../context/AuthContext";



const TODAY =
new Date()
.toISOString()
.slice(0,10);



const EMPTY_PAYMENT = {

    invoice:"",
    amount:"",
    method:"CASH",
    reference_number:"",
    paid_on:TODAY

};





export default function PaymentsPage(){


const {user}=useAuth();


const isTenant =
user?.role === "TENANT";



const [invoices,setInvoices]=useState([]);

const [payments,setPayments]=useState([]);

const [loading,setLoading]=useState(true);

const [selectedInvoice,setSelectedInvoice]=useState(null);

const [paymentDrawer,setPaymentDrawer]=useState(false);

const [paymentForm,setPaymentForm]=useState(
    {...EMPTY_PAYMENT}
);

const [error,setError]=useState("");


const [showInvoices,setShowInvoices]=useState(false);

const [showHistory,setShowHistory]=useState(false);




async function load(){


try{


setLoading(true);


const [
invoiceRes,
paymentRes
]=await Promise.all([

client.get("/payments/invoices/"),

client.get("/payments/")

]);


setInvoices(
invoiceRes.data.results ??
invoiceRes.data
);


setPayments(
paymentRes.data.results ??
paymentRes.data
);



}

catch(err){

console.log(err);

setError(
err.response?.data?.detail ||
"Unable to load payments"
);


}

finally{

setLoading(false);

}


}





useEffect(()=>{

load();

},[]);





function chooseInvoice(invoice){

setSelectedInvoice(invoice);

}






function selectInvoice(e){


const id=e.target.value;


const invoice=invoices.find(
i=>i.id===Number(id)
);



setPaymentForm({

...paymentForm,

invoice:id,

amount:
invoice?.outstanding_balance || ""

});


}



async function recordPayment() {
  try {
    await client.post(
    `/payments/invoices/${paymentForm.invoice}/record-payment/`,
    {
        amount: paymentForm.amount,
        method: paymentForm.method,
        paid_on: paymentForm.paid_on,
        reference_number: paymentForm.reference_number,
        notes: paymentForm.notes,
    }
    );

    // Notify dashboard to refresh
    window.dispatchEvent(new Event("dashboard-refresh"));

    setPaymentDrawer(false);

    setPaymentForm({
      ...EMPTY_PAYMENT,
    });

    load();
  } catch (err) {
    alert(JSON.stringify(err.response?.data));
  }
}





function downloadReceipt(payment){


const receiptWindow =
window.open(
"",
"_blank"
);



receiptWindow.document.write(`

<html>

<head>

<title>
Receipt ${payment.receipt_number}
</title>

<style>

body{
font-family:Arial;
padding:40px;
}

.receipt{
border:1px solid #ddd;
padding:30px;
width:400px;
}

h2{
text-align:center;
}

.row{
margin:10px 0;
}

</style>

</head>


<body>


<div class="receipt">


<h2>
Nestled Hostel
</h2>


<hr/>


<div class="row">
<strong>Receipt:</strong>
${payment.receipt_number}
</div>


<div class="row">
<strong>Tenant Name:</strong>
${payment.tenant_name || "N/A"}
</div>


<div class="row">
<strong>Email:</strong>
${payment.tenant_email || "N/A"}
</div>


<div class="row">
<strong>Phone:</strong>
${payment.tenant_phone || "N/A"}
</div>


<div class="row">
<strong>Room:</strong>
${payment.room_number || "N/A"}
</div>


<div class="row">
<strong>Bed:</strong>
${payment.bed_number || "N/A"}
</div>


<div class="row">
<strong>Amount:</strong>
Rs ${payment.amount}
</div>


<div class="row">
<strong>Method:</strong>
${payment.method}
</div>


<div class="row">
<strong>Date:</strong>
${payment.paid_on}
</div>


<hr/>


<p>
Thank you for your payment.
</p>


</div>


<script>

window.print();

</script>


</body>

</html>

`);


receiptWindow.document.close();


}






const collected =
payments.reduce(
(sum,p)=>
sum+
Number(p.amount||0),
0
);



const outstanding =
invoices.reduce(
(sum,i)=>
sum+
Number(i.outstanding_balance||0),
0
);



const pendingInvoices =
invoices.filter(
i=>
Number(i.outstanding_balance)>0
);



const currentInvoice =
pendingInvoices[0];



const lastPayment =
payments[0];
return (

<Layout>


<div className="space-y-6">



<div className="
flex
justify-between
items-center
">


<div>

<h1 className="text-2xl font-bold">

{
isTenant
?
"My Payments"
:
"Payments"
}


</h1>



<p className="text-gray-500">

{
isTenant
?
"Manage your hostel rent and payment history"
:
"Manage hostel rent payments"
}


</p>


</div>





{
!isTenant &&


<button

onClick={()=>
setPaymentDrawer(true)
}


className="
bg-green-600
text-white
px-4
py-2
rounded-lg
flex
gap-2
"


>


<CreditCard size={18}/>


Record Payment


</button>


}



</div>








{
error &&

<div className="
bg-red-100
text-red-700
p-3
rounded
">

{error}

</div>

}









<div className="
grid
md:grid-cols-3
gap-4
">



<StatCard

label="Invoices"

value={invoices.length}

/>




<StatCard

label={
isTenant
?
"Amount Due"
:
"Collected"
}


value={
isTenant
?
`Rs ${outstanding}`
:
`Rs ${collected}`
}

/>




{
isTenant &&


<StatCard

label="Status"

value={
currentInvoice?.status || "PAID"
}

/>


}




{
!isTenant &&


<StatCard

label="Pending Collection"

value={`Rs ${outstanding}`}

/>


}



</div>













{
isTenant &&


<div className="card p-5">


<h2 className="text-lg font-bold mb-4">

Upcoming Payment

</h2>




{
currentInvoice ?


<div className="space-y-3">


<div className="
flex
justify-between
">

<span className="text-gray-500">
Amount Due
</span>


<strong>
Rs {currentInvoice.outstanding_balance}
</strong>


</div>




<div className="
flex
justify-between
">


<span className="text-gray-500">
Due Date
</span>


<strong>
{currentInvoice.due_date}
</strong>


</div>





<div className="
flex
justify-between
">


<span className="text-gray-500">
Status
</span>


<strong>
{currentInvoice.status}
</strong>


</div>





<button

onClick={()=>
chooseInvoice(currentInvoice)
}


className="
bg-green-600
text-white
px-4
py-2
rounded-lg
w-full
"


>

Pay Rent

</button>



</div>



:

<div className="
text-gray-500
">

No pending rent payment.

</div>


}


</div>


}









{
!isTenant &&

<>

<PaymentQRManager />

<PaymentApproval />

</>

}









{
!isTenant &&


<div className="card p-5">


<div className="
flex
justify-between
items-center
mb-4
">


<h2 className="text-lg font-bold">

Pending Collections

</h2>



<button

onClick={()=>
setShowInvoices(!showInvoices)
}

className="
text-green-600
font-semibold
"

>

{
showInvoices
?
"Show Less"
:
"View All"
}


</button>


</div>





<DataTable


rows={

showInvoices

?

pendingInvoices

:

pendingInvoices.slice(0,5)

}


columns={[


{
key:"tenant_email",
header:"Tenant"
},


{
key:"outstanding_balance",
header:"Amount Due"
},


{
key:"due_date",
header:"Due"
}


]}


/>



</div>


}









{
isTenant &&
selectedInvoice &&

<TenantPaymentSubmission

invoice={selectedInvoice}

/>

}
<div className="card p-5">


<div className="
flex
justify-between
items-center
mb-4
">


<h2 className="text-lg font-bold">

{
isTenant
?
"My Payment History"
:
"Payment History"
}


</h2>



<button

onClick={()=>
setShowHistory(!showHistory)
}

className="
text-green-600
font-semibold
"

>

{
showHistory
?
"Show Less"
:
"View Full History"
}


</button>


</div>





<DataTable


rows={

showHistory

?

payments

:

payments.slice(0,5)

}


columns={[


{
key:"receipt_number",
header:"Receipt"
},


{
key:"amount",
header:"Amount"
},


{
key:"method",
header:"Method"
},


{
key:"paid_on",
header:"Date"
},



{

key:"download",

header:"Receipt",

render:(row)=>(


<button

onClick={()=>
downloadReceipt(row)
}


className="
bg-blue-600
text-white
px-3
py-1
rounded
flex
items-center
gap-2
"


>


<Download size={16}/>


Download


</button>


)

}


]}



/>


</div>









{
!isTenant &&


<FormDrawer

open={paymentDrawer}

title="Record Payment"

onClose={()=>
setPaymentDrawer(false)
}


>


<div className="space-y-4">



<select

className="
border
p-3
w-full
rounded
"


onChange={selectInvoice}


>


<option>

Select Invoice

</option>



{

invoices.map(inv=>(


<option

key={inv.id}

value={inv.id}

>

{inv.tenant_email}

-
Rs {inv.outstanding_balance}


</option>


))


}


</select>






<input

className="
border
p-3
w-full
rounded
"


placeholder="Amount"


value={paymentForm.amount}


onChange={
e=>

setPaymentForm({

...paymentForm,

amount:e.target.value

})

}


/>






<button

onClick={recordPayment}


className="
bg-green-600
text-white
w-full
p-3
rounded-lg
"


>

Save Payment


</button>


</div>


</FormDrawer>


}




</div>


</Layout>


);


}
import {
    useEffect,
    useState
} from "react";


import {
    CreditCard,
    Receipt
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





const [invoices,setInvoices]=
useState([]);


const [payments,setPayments]=
useState([]);


const [loading,setLoading]=
useState(true);


const [selectedInvoice,setSelectedInvoice]=
useState(null);


const [paymentDrawer,setPaymentDrawer]=
useState(false);


const [paymentForm,setPaymentForm]=
useState(
{
...EMPTY_PAYMENT
}
);


const [error,setError]=
useState("");









async function load(){


try{


setLoading(true);



const [
invoiceRes,
paymentRes
]=await Promise.all([


client.get(
"/payments/invoices/"
),


client.get(
"/payments/"
)


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


const id =
e.target.value;



const invoice =
invoices.find(
i=>i.id === Number(id)
);



setPaymentForm({

...paymentForm,

invoice:id,

amount:
invoice?.outstanding_balance || ""

});


}









async function recordPayment(){


try{


await client.post(

"/payments/",

paymentForm

);



setPaymentDrawer(false);



setPaymentForm(
{
...EMPTY_PAYMENT
}
);



load();


}


catch(err){


alert(
JSON.stringify(
err.response?.data
)
);


}



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
Number(
i.outstanding_balance||0
),
0
);










const invoiceColumns=[


{

key:"tenant_email",

header:"Tenant"

},


{

key:"due_date",

header:"Due"

},


{

key:"total_amount",

header:"Total"

},


{

key:"amount_paid",

header:"Paid"

},


{

key:"outstanding_balance",

header:"Balance"

},


{

key:"status",

header:"Status"

},



{

key:"action",

header:"Action",

render:(row)=>

isTenant &&

<button

onClick={()=>
chooseInvoice(row)
}

className="
bg-green-600
text-white
px-3
py-1
rounded
"

>

Pay

</button>


}



];









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
"Pay your hostel rent online"
:
"Manage hostel rent payments"
}

</p>


</div>





{
!isTenant &&

<div className="flex gap-3">


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


</div>

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



</div>









{
!isTenant &&

<>


<PaymentQRManager />


<PaymentApproval />


</>

}









<div className="card p-5">


<h2 className="text-lg font-bold mb-4">

Invoices

</h2>



<DataTable

rows={invoices}

columns={invoiceColumns}

loading={loading}

/>


</div>









{
isTenant &&
selectedInvoice &&

<TenantPaymentSubmission

invoice={selectedInvoice}

/>

}









<div className="card p-5">


<h2 className="text-lg font-bold mb-4">

Payment History

</h2>



<DataTable

rows={payments}

columns={[


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

value={
paymentForm.amount
}

onChange={e=>

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
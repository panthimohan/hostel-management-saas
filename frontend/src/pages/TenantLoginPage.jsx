import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CheckCircle } from "lucide-react";

import { useAuth } from "../context/AuthContext";


export default function TenantLoginPage() {


  const { login } = useAuth();
  const navigate = useNavigate();


  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [error,setError] = useState("");
  const [submitting,setSubmitting] = useState(false);



  async function handleSubmit(e){

    e.preventDefault();

    setError("");
    setSubmitting(true);


    try {

      await login(
        email,
        password
      );


      navigate("/");


    } catch(err){


      if(err.response){

        setError(
          JSON.stringify(
            err.response.data,
            null,
            2
          )
        );


      } else {

        setError(
          "Login failed"
        );

      }


    } finally {

      setSubmitting(false);

    }

  }



return (

<div
className="
min-h-screen
grid
lg:grid-cols-2
bg-gray-50
">


{/* LEFT SIDE */}


<div
className="
hidden
lg:flex
flex-col
justify-between
p-12
text-white
bg-gradient-to-br
from-[#071426]
via-[#12304a]
to-[#065f46]
">


<div>


<h1
className="
text-5xl
font-extrabold
text-white
tracking-tight
"
>

Nestled

</h1>


<p
className="
mt-3
text-xl
font-medium
text-white/90
"
>

Your hostel life,
organized simply.

</p>


</div>




<div>


<h2
className="
text-6xl
font-extrabold
leading-[1.05]
text-white
"
>

Your room.

<br/>


<span
className="
text-green-300
"
>

Your payments.

</span>


<br/>

Your stay.


</h2>




<p
className="
mt-8
text-xl
leading-relaxed
text-white/90
max-w-xl
"
>

Access your rent details,
payment history,
notices, and hostel services
from one simple dashboard.

</p>





<div
className="
mt-10
rounded-2xl
border
border-white/20
bg-white/10
backdrop-blur-sm
p-6
"
>


<h3
className="
text-xl
font-bold
mb-5
text-white
"
>

Tenant Dashboard

</h3>



<div
className="
grid
grid-cols-3
gap-4
"
>


<DashboardCard

title="Room"

value="A-101"

/>



<DashboardCard

title="Rent"

value="Paid"

/>



<DashboardCard

title="Status"

value="Active"

/>


</div>



</div><div
className="
grid
grid-cols-2
gap-4
mt-8
"
>


<Benefit
text="View Rent Payments"
/>


<Benefit
text="Check Room Details"
/>


<Benefit
text="Receive Hostel Notices"
/>


<Benefit
text="Access Hostel Services"
/>


</div>




</div>





<p
className="
text-sm
text-white/80
"
>

© {new Date().getFullYear()} Nestled

</p>




</div>







{/* RIGHT SIDE */}



<div
className="
flex
items-start
justify-center
p-6
lg:p-14
"
>



<div
className="
w-full
max-w-md
"
>




<div
className="
bg-white
rounded-2xl
shadow-xl
p-8
"
>



<h1
className="
text-3xl
font-bold
text-gray-900
"
>

Welcome back 👋

</h1>



<p
className="
mt-2
mb-6
text-gray-600
"
>

Login to access your hostel account.

</p>







<form

onSubmit={handleSubmit}

className="
space-y-5
"

>




<div>


<label
className="
text-sm
font-semibold
text-gray-700
"
>

Email

</label>




<input

className="
input
w-full
mt-1
"

type="email"

placeholder="tenant@example.com"

value={email}

onChange={
e=>setEmail(e.target.value)
}

required

/>

</div>







<div>


<label
className="
text-sm
font-semibold
text-gray-700
"
>

Password

</label>





<input

className="
input
w-full
mt-1
"

type="password"

placeholder="••••••••"

value={password}

onChange={
e=>setPassword(e.target.value)
}

required

/>


</div>







<div
className="
text-right
"
>


<Link

to="/forgot-password"

className="
text-sm
text-primary
font-semibold
"

>

Forgot Password?

</Link>


</div>







{
error && (

<div
className="
bg-red-50
border
border-red-200
text-red-600
rounded-lg
p-3
text-sm
"
>

{error}

</div>

)

}







<button


type="submit"


disabled={submitting}


className="
btn-primary
w-full
py-3
rounded-xl
font-semibold
"


>


{

submitting

?

"Logging in..."

:

"Log in"

}


</button>





</form>







<div
className="
mt-6
text-center
space-y-3
"
>



<p
className="
text-gray-700
"
>

Hostel owner?


<Link

to="/login"

className="
text-primary
font-semibold
ml-1
"

>

Login here

</Link>


</p>





<p
className="
text-gray-700
"
>

Need help?


<span
className="
text-primary
font-semibold
ml-1
"
>

Contact your hostel manager

</span>


</p>




</div>




</div>





<div
className="
mt-8
bg-white
rounded-2xl
shadow-md
p-7
"
>



<h2
className="
text-xl
font-bold
text-gray-900
"
>

Tenant features

</h2>





<div
className="
mt-5
space-y-4
"
>


<InfoItem

text="View your room allocation"

/>


<InfoItem

text="Track monthly rent payments"

/>


<InfoItem

text="Receive hostel announcements"

/>


<InfoItem

text="Access payment history"

/>


</div>




</div>




</div>



</div>



</div>

);


}function DashboardCard({title,value}){


  return (

    <div
    className="
      bg-white/20
      backdrop-blur-sm
      rounded-xl
      p-4
      border
      border-white/20
    "
    >


      <p
      className="
        text-white/80
        text-sm
        font-medium
      "
      >

        {title}

      </p>



      <p
      className="
        text-white
        text-2xl
        font-bold
        mt-2
      "
      >

        {value}

      </p>



    </div>

  );


}







function Benefit({text}){


  return (

    <div
    className="
      flex
      items-center
      gap-2
      text-white
    "
    >


      <CheckCircle

        size={18}

        className="
          text-green-300
        "

      />



      <span
      className="
        text-white/90
      "
      >

        {text}

      </span>



    </div>


  );


}







function InfoItem({text}){


  return (

    <div
    className="
      flex
      items-center
      gap-3
      text-gray-700
    "
    >


      <div
      className="
        h-2
        w-2
        rounded-full
        bg-green-500
      "
      >


      </div>




      <span
      className="
        font-medium
      "
      >

        {text}

      </span>



    </div>


  );


}
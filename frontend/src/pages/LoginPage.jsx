import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CheckCircle } from "lucide-react";

import { useAuth } from "../context/AuthContext";


export default function LoginPage() {


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



    try{


      await login(
        email,
        password
      );


      navigate("/");


    }


    catch(err){


      if(err.response){


        setError(
          JSON.stringify(
            err.response.data,
            null,
            2
          )
        );


      }

      else{


        setError(
          "Login failed"
        );


      }


    }


    finally{


      setSubmitting(false);


    }


  }







  return (

    <div className="
      min-h-screen
      grid
      lg:grid-cols-2
      bg-gray-50
    ">





      {/* LEFT SIDE */}





      <div className="
        hidden
        lg:flex
        flex-col
        justify-between
        bg-[#071426]
        p-12
        text-white
      ">






        <div>


          <h1 className="
            text-5xl
            font-extrabold
            text-white
          ">

            Nestled

          </h1>





          <p className="
            mt-3
            text-xl
            font-medium
            text-white
          ">

            Hostel management made simple.

          </p>



        </div>








        <div>




          <h2 className="
            text-6xl
            font-extrabold
            leading-[1.05]
            text-white
          ">


            Every room.

            <br/>



            <span className="
              text-green-400
            ">

              Every tenant.

            </span>



            <br/>


            Every payment.



          </h2>







          <p className="
            mt-8
            text-xl
            leading-relaxed
            max-w-xl
            text-white
          ">


            Manage rooms, tenants,
            rent payments, expenses,
            and reports from one powerful
            hostel management platform.


          </p>







          <div className="
            mt-10
            rounded-2xl
            border
            border-white/20
            bg-white/10
            p-6
          ">



            <h3 className="
              text-xl
              font-bold
              mb-5
              text-white
            ">


              Hostel Dashboard


            </h3>





            <div className="
              grid
              grid-cols-3
              gap-4
            ">



              <DashboardCard

                title="Rooms"

                value="150"

              />



              <DashboardCard

                title="Tenants"

                value="128"

              />



              <DashboardCard

                title="Revenue"

                value="8.4L"

              />



            </div>



          </div>




          <div className="
            grid
            grid-cols-2
            gap-4
            mt-8
          ">



            <Benefit text="Room & Bed Management"/>

            <Benefit text="Tenant Management"/>

            <Benefit text="Digital Rent Payments"/>

            <Benefit text="Reports & Analytics"/>



          </div>








          <div className="
            mt-8
            rounded-xl
            bg-green-500/20
            border
            border-green-400/40
            p-6
          ">




            <p className="
              text-green-300
              font-bold
              text-xl
            ">


              🚀 Launch Offer


            </p>





            <p className="
              mt-2
              text-white
              font-medium
            ">


              First 100 hostels get 50% OFF


            </p>







            <p className="
              mt-3
              text-4xl
              font-extrabold
              text-white
            ">


              NPR 5,000/year


            </p>







            <p className="
              mt-1
              text-white
            ">


              Regular price NPR 10,000/year


            </p>





          </div>







        </div>








        <p className="
          text-sm
          text-white
        ">


          © {new Date().getFullYear()} Nestled


        </p>





      </div>













      {/* RIGHT SIDE */}





      <div className="
        flex
        items-start
        justify-center
        p-8
        lg:p-14
      ">





        <div className="
          w-full
          max-w-md
        ">







          {/* LOGIN FORM */}




          <div className="
            bg-white
            rounded-2xl
            shadow-xl
            p-8
          ">




            <h1 className="
              text-3xl
              font-bold
              text-gray-900
            ">


              Welcome back 👋


            </h1>







            <p className="
              mt-2
              mb-6
              text-gray-500
            ">


              Login to manage your hostel.


            </p>







            <form

              onSubmit={handleSubmit}

              className="
                space-y-5
              "

            >






              <div>


                <label className="
                  text-sm
                  font-medium
                  text-gray-700
                ">


                  Email


                </label>






                <input


                  className="
                    input
                    w-full
                    mt-1
                  "



                  type="email"



                  placeholder="owner@example.com"



                  value={email}



                  onChange={
                    e=>setEmail(e.target.value)
                  }



                  required



                />



              </div>









              <div>


                <label className="
                  text-sm
                  font-medium
                  text-gray-700
                ">


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
              

                            <div className="text-right">

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


                  <div className="
                    bg-red-50
                    text-red-600
                    rounded-lg
                    p-3
                    text-sm
                  ">


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


            <div className="
              mt-6
              text-center
              space-y-3
            ">




              <p className="
                text-gray-700
              ">


                New hostel business?


                <Link

                  to="/owner-signup"

                  className="
                    text-primary
                    font-semibold
                    ml-1
                  "

                >

                  Register your hostel

                </Link>



              </p>








              <p className="
                text-gray-700
              ">


                Tenant?


                <Link

                  to="/tenant/login"

                  className="
                    text-primary
                    font-semibold
                    ml-1
                  "

                >

                  Login here

                </Link>



              </p>






            </div>





          </div>









          {/* INFORMATION CARD */}





          <div className="
            mt-8
            bg-white
            rounded-2xl
            shadow-md
            p-7
          ">





            <h2 className="
              text-xl
              font-bold
              text-gray-900
            ">


              Why hostel owners choose Nestled


            </h2>








            <div className="
              mt-5
              space-y-4
            ">



              <InfoItem

                text="Manage rooms and beds easily"

              />




              <InfoItem

                text="Track tenants and rent payments"

              />




              <InfoItem

                text="Accept digital payments"

              />




              <InfoItem

                text="View hostel reports and analytics"

              />




            </div>









            <div className="
              mt-6
              bg-green-50
              rounded-xl
              p-5
            ">





              <p className="
                font-bold
                text-green-700
              ">


                🚀 Founding Partner Offer


              </p>







              <p className="
                mt-2
                text-gray-700
              ">


                First 100 hostels get


              </p>







              <p className="
                text-3xl
                font-extrabold
                text-green-700
              ">


                NPR 5,000/year


              </p>







              <p className="
                text-sm
                text-gray-500
              ">


                50% OFF launch pricing


              </p>





            </div>







          </div>







        </div>






      </div>






    </div>


  );


}









function DashboardCard({title,value}){


  return (

    <div className="
      bg-white/20
      rounded-xl
      p-4
    ">



      <p className="
        text-white
        text-sm
      ">


        {title}


      </p>





      <p className="
        text-white
        text-2xl
        font-bold
        mt-2
      ">


        {value}


      </p>



    </div>

  );


}









function Benefit({text}){


  return (

    <div className="
      flex
      items-center
      gap-2
      text-white
    ">



      <CheckCircle

        size={18}

        className="
          text-green-400
        "

      />




      <span>

        {text}

      </span>




    </div>

  );


}









function InfoItem({text}){


  return (

    <div className="
      flex
      items-center
      gap-3
      text-gray-700
    ">



      <div className="
        h-2
        w-2
        rounded-full
        bg-green-500
      ">



      </div>





      <span>

        {text}

      </span>





    </div>

  );


}
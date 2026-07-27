import { useEffect, useState } from "react";
import { CreditCard, Download } from "lucide-react";

import client from "../api/client";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import TenantPaymentSubmission from "../components/TenantPaymentSubmission";


export default function TenantDashboard() {


  const [room, setRoom] = useState(null);

  const [invoice, setInvoice] = useState(null);

  const [payments, setPayments] = useState([]);

  const [loading, setLoading] = useState(true);

  const [showPayment, setShowPayment] = useState(false);




  useEffect(() => {


    async function load(){


      try{


        const [
          roomRes,
          invoiceRes,
          paymentRes
        ] = await Promise.all([


          client.get("/beds/my-room/"),


          client.get("/payments/invoices/"),


          client.get("/payments/")


        ]);



        setRoom(roomRes.data);



        const invoices =
          invoiceRes.data.results ??
          invoiceRes.data;



        const unpaidInvoice =
          invoices.find(
            inv =>
              inv.status !== "PAID"
          );



        setInvoice(
          unpaidInvoice || null
        );




        const paymentData =
          paymentRes.data.results ??
          paymentRes.data;



        setPayments(
          paymentData.slice(0,5)
        );


      }

      catch(err){

        console.log(err);

      }

      finally{

        setLoading(false);

      }


    }



    load();


  },[]);






  function downloadReceipt(payment){


    const win =
      window.open(
        "",
        "_blank"
      );



    win.document.write(`

    <html>

    <body style="font-family:Arial;padding:40px">


    <h2>Nestled Hostel</h2>

    <hr/>


    <p>
    Receipt: ${payment.receipt_number}
    </p>


    <p>
    Amount: Rs ${payment.amount}
    </p>


    <p>
    Method: ${payment.method}
    </p>


    <p>
    Date: ${payment.paid_on}
    </p>


    <script>
    window.print();
    </script>


    </body>

    </html>

    `);



    win.document.close();


  }







  if(loading){


    return (

      <Layout>

        <div className="card p-10 text-center">

          Loading...

        </div>


      </Layout>

    );


  }








  return (


    <Layout>


      <div className="space-y-8">



        <div>


          <h1 className="font-display text-2xl font-semibold">

            My Dashboard

          </h1>



          <p className="text-sm text-ink-soft mt-1">

            Your room, rent and payment information.

          </p>


        </div>







        <div className="grid md:grid-cols-3 gap-4">


          <StatCard

            label="Current Due"

            value={
              invoice
              ?
              `Rs ${invoice.rent_amount}`
              :
              "Rs 0"
            }

          />



          <StatCard

            label="Due Date"

            value={
              invoice?.due_date || "-"
            }

          />



          <StatCard

            label="Last Payment"

            value={
              payments.length
              ?
              `Rs ${payments[0].amount}`
              :
              "No payment"
            }

          />


        </div>








        <div className="card p-6">


          <h2 className="font-display text-lg font-semibold mb-4">

            My Room

          </h2>




          {
            room?.current ?


            <>


            <p className="text-xs uppercase text-ink-soft">

              {room.current.hostel_name}

            </p>



            <p className="font-display text-3xl mt-2">

              Room {room.current.room_number}

              <span className="text-lg text-ink-soft ml-2">

                Bed {room.current.bed_number}

              </span>

            </p>




            <div className="mt-4 grid grid-cols-2 gap-4 text-sm">


              <div>

                <p className="text-ink-soft">
                Room Type
                </p>

                <p>
                {room.current.room_type}
                </p>

              </div>




              <div>

                <p className="text-ink-soft">
                Monthly Rent
                </p>

                <p>
                Rs {room.current.price}
                </p>

              </div>


            </div>


            </>


            :


            <p>
            No active room assigned.
            </p>


          }


        </div>









        <div className="card p-6">


          <h2 className="font-display text-lg font-semibold">

            Outstanding Rent

          </h2>




          <p className="text-4xl font-bold mt-3">

            Rs {
              invoice?.rent_amount || 0
            }

          </p>



          <p className="text-sm text-ink-soft mt-2">

            Due on {invoice?.due_date || "-"}

          </p>





          <button


            onClick={()=>
              setShowPayment(true)
            }


            className="
            mt-5
            bg-green-600
            text-white
            px-5
            py-3
            rounded-lg
            flex
            items-center
            gap-2
            "


            disabled={!invoice}


          >


            <CreditCard size={18}/>


            Pay Rent


          </button>



        </div>









        {
          showPayment &&
          invoice &&


          <TenantPaymentSubmission

            invoice={invoice}

          />


        }









        <div className="card p-6">


          <h2 className="font-display text-lg font-semibold mb-4">

            Recent Payments

          </h2>




          <div className="space-y-3">


          {
            payments.map(payment=>(


              <div

                key={payment.id}

                className="
                flex
                justify-between
                items-center
                border-b
                pb-3
                "


              >



                <div>


                  <p className="font-medium">

                    Rs {payment.amount}

                  </p>



                  <p className="text-sm text-ink-soft">

                    {payment.method}
                    {" · "}
                    {payment.paid_on}

                  </p>


                </div>





                <button


                  onClick={()=>
                    downloadReceipt(payment)
                  }



                  className="
                  text-sm
                  text-blue-600
                  flex
                  gap-1
                  items-center
                  "


                >


                  <Download size={15}/>


                  Receipt


                </button>



              </div>


            ))
          }


          {
            payments.length===0 &&


            <p className="text-sm text-ink-soft">

              No payments yet.

            </p>


          }


          </div>


        </div>





      </div>


    </Layout>


  );


}
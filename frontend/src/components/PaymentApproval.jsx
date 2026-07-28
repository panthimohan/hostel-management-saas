import {
    useEffect,
    useState
} from "react";

import {
    Check,
    X,
    Eye
} from "lucide-react";

import client from "../api/client";



export default function PaymentApproval(){


    const [payments,setPayments] = useState([]);

    const [loading,setLoading] = useState(true);

    const [processing,setProcessing] = useState(null);





    async function loadPayments(){

        try{

            setLoading(true);


            const res = await client.get(
                "/payments/payment-submissions/"
            );


            const data =
                res.data.results ?? res.data;



            setPayments(
                data.filter(
                    payment =>
                    payment.status === "PENDING"
                )
            );


        }
        catch(error){

            console.error(
                "Loading payment submissions failed:",
                error
            );

        }
        finally{

            setLoading(false);

        }

    }





    useEffect(()=>{

        loadPayments();

    },[]);






    async function approve(id){


        const confirmApprove =
            window.confirm(
                "Approve this payment?"
            );


        if(!confirmApprove)
            return;




        try{


            setProcessing(id);



            await client.post(

                `/payments/payment-submissions/${id}/approve/`

            );



            alert(
                "Payment approved successfully"
            );



            await loadPayments();



        }
        catch(error){


            console.error(
                error.response?.data || error
            );


            alert(
                "Payment approval failed"
            );


        }
        finally{

            setProcessing(null);

        }

    }








    async function reject(id){


        const remarks =
            window.prompt(
                "Reason for rejection?"
            );



        try{


            setProcessing(id);



            await client.post(

                `/payments/payment-submissions/${id}/reject/`,

                {
                    remarks:
                    remarks || ""
                }

            );



            alert(
                "Payment rejected"
            );



            await loadPayments();



        }
        catch(error){


            console.error(
                error.response?.data || error
            );


            alert(
                "Payment rejection failed"
            );


        }
        finally{

            setProcessing(null);

        }

    }








    function imageUrl(path){


        if(!path)
            return null;



        if(path.startsWith("http"))
            return path;



        return `https://traversedw.com.np${path}`;

    }









    if(loading){

        return (

            <div className="
                bg-white
                rounded-xl
                shadow
                p-6
            ">

                Loading payment approvals...

            </div>

        );

    }









    return (

        <div className="
            bg-white
            rounded-xl
            shadow
            p-6
        ">



            <div className="
                flex
                justify-between
                items-center
                mb-6
            ">



                <h2 className="
                    text-xl
                    font-bold
                ">

                    Pending Payment Approvals

                </h2>




                <span className="
                    bg-yellow-100
                    text-yellow-700
                    px-4
                    py-1
                    rounded-full
                    font-semibold
                ">

                    {payments.length}

                </span>



            </div>








            {
                payments.length === 0 &&

                <div className="
                    text-gray-500
                    text-center
                    py-10
                ">

                    No pending payments.

                </div>

            }









            <div className="
                space-y-5
            ">



            {
                payments.map(payment=>(


                    <div

                    key={payment.id}

                    className="
                        border
                        rounded-xl
                        p-5
                        grid
                        lg:grid-cols-5
                        gap-5
                        items-center
                    "

                    >





                        <div>


                            <p className="
                                font-bold
                            ">

                                {payment.tenant_email}

                            </p>


                            <p className="
                                text-sm
                                text-gray-500
                            ">

                                {payment.invoice_number}

                            </p>


                        </div>







                        <div>


                            <p className="
                                text-sm
                                text-gray-500
                            ">

                                Amount

                            </p>


                            <p className="
                                font-bold
                                text-lg
                            ">

                                Rs {payment.amount}

                            </p>


                            <p className="
                                text-sm
                            ">

                                TXN:
                                {" "}
                                {payment.transaction_id}

                            </p>


                        </div>








                        <div>


                        {
                            payment.screenshot &&

                            <a

                            href={imageUrl(payment.screenshot)}

                            target="_blank"

                            rel="noreferrer"

                            >

                                <img

                                src={
                                    imageUrl(
                                        payment.screenshot
                                    )
                                }

                                className="
                                    h-32
                                    w-32
                                    object-cover
                                    rounded-lg
                                    border
                                "

                                />

                            </a>

                        }


                        </div>








                        <div className="
                            lg:col-span-2
                            flex
                            gap-3
                        ">



                            <button

                            disabled={
                                processing === payment.id
                            }

                            onClick={()=>
                                approve(payment.id)
                            }

                            className="
                                bg-green-600
                                text-white
                                px-5
                                py-3
                                rounded-lg
                                flex
                                items-center
                                gap-2
                            "

                            >

                                <Check size={18}/>

                                {
                                    processing === payment.id
                                    ?
                                    "Processing..."
                                    :
                                    "Approve"
                                }


                            </button>








                            <button

                            disabled={
                                processing === payment.id
                            }

                            onClick={()=>
                                reject(payment.id)
                            }

                            className="
                                bg-red-600
                                text-white
                                px-5
                                py-3
                                rounded-lg
                                flex
                                items-center
                                gap-2
                            "

                            >

                                <X size={18}/>

                                Reject


                            </button>





                        </div>





                    </div>


                ))

            }



            </div>



        </div>

    );


}

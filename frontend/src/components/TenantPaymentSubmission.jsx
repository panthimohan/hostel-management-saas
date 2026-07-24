import {
    useEffect,
    useState
} from "react";

import client from "../api/client";



export default function TenantPaymentSubmission({ invoice }) {


    const [qrs, setQrs] = useState([]);

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({

        invoice: "",

        payment_qr: "",

        amount: "",

        transaction_id: "",

        screenshot: null

    });






    useEffect(() => {

        if (!invoice)
            return;


        setForm({

            invoice: invoice.id,

            payment_qr: "",

            amount: "",

            transaction_id: "",

            screenshot: null

        });


        loadQR();


    }, [invoice]);









    async function loadQR() {


        try {


            const res = await client.get(
                "/payments/payment-qrs/"
            );


            setQrs(
                res.data.results ?? res.data
            );


        }

        catch(error) {


            console.error(
                "Payment account loading error",
                error
            );


        }


    }









    function change(e) {


        setForm({

            ...form,

            [e.target.name]:
            e.target.value

        });


    }








    function fileChange(e) {


        setForm({

            ...form,

            screenshot:
            e.target.files[0]

        });


    }









    function qrImage(path) {


        if (!path)
            return "";


        if (path.startsWith("http"))
            return path;


        return `http://localhost:8000${path}`;

    }









    async function submitPayment() {



        const amount =
            Number(form.amount);



        const balance =
            Number(
                invoice.outstanding_balance
            );




        if (!form.payment_qr) {


            alert(
                "Please select where you paid"
            );

            return;

        }





        if (!amount || amount <= 0) {


            alert(
                "Enter valid amount"
            );

            return;

        }





        if (amount > balance) {


            alert(
                `Maximum payable amount is Rs ${balance}`
            );

            return;

        }






        if (!form.transaction_id) {


            alert(
                "Enter transaction ID"
            );

            return;

        }





        if (!form.screenshot) {


            alert(
                "Upload payment screenshot"
            );

            return;

        }






        const data = new FormData();



        Object.entries(form)
        .forEach(([key,value]) => {


            if (value) {

                data.append(
                    key,
                    value
                );

            }


        });







        try {


            setLoading(true);



            await client.post(

                "/payments/payment-submissions/",

                data,

                {

                    headers: {

                        "Content-Type":
                        "multipart/form-data"

                    }

                }

            );




            alert(
                "Payment proof submitted successfully"
            );




            setForm({

                invoice: invoice.id,

                payment_qr: "",

                amount: "",

                transaction_id: "",

                screenshot: null

            });



        }

        catch(error) {


            console.error(
                error.response?.data
            );


            alert(
                JSON.stringify(
                    error.response?.data
                )
            );


        }

        finally {


            setLoading(false);


        }


    }








    if (!invoice)
        return null;








    return (


        <div className="
            border
            rounded-xl
            p-6
            mt-6
            bg-white
        ">




            <h2 className="
                text-xl
                font-bold
                mb-4
            ">

                Pay Invoice #{invoice.invoice_number}

            </h2>







            <p className="mb-5">

                Amount Due:

                <b>
                    Rs {invoice.outstanding_balance}
                </b>

            </p>







            <h3 className="
                font-semibold
                mb-4
            ">

                I paid using

            </h3>








            <div className="
                grid
                md:grid-cols-3
                gap-5
            ">



            {
                qrs.map(qr => (



                    <div


                    key={qr.id}



                    onClick={() =>


                        setForm({

                            ...form,

                            payment_qr:
                            qr.id

                        })


                    }



                    className={`

                    border

                    rounded-xl

                    p-5

                    cursor-pointer

                    transition


                    ${
                        Number(form.payment_qr)
                        ===
                        qr.id

                        ?

                        "border-blue-600 bg-blue-50"

                        :

                        "hover:border-gray-400"

                    }


                    `}



                    >




                        <h4 className="
                            font-bold
                            text-lg
                        ">

                            {qr.payment_type}

                        </h4>





                        <p className="
                            text-sm
                            mt-1
                        ">

                            {qr.title}

                        </p>








                        {
                            qr.qr_image &&


                            <img


                            src={
                                qrImage(
                                    qr.qr_image
                                )
                            }


                            className="
                                h-40
                                w-full
                                object-contain
                                my-4
                                border
                                rounded
                            "


                            />

                        }







                        <p className="text-sm">

                            {qr.account_name}

                        </p>




                        {
                            qr.account_number &&


                            <p className="
                                text-sm
                                text-gray-500
                            ">

                                {qr.account_number}

                            </p>


                        }



                    </div>



                ))

            }



            </div>








            {
                qrs.length === 0 &&


                <p className="
                    text-red-500
                    mt-4
                ">

                    No payment accounts configured by hostel.

                </p>

            }









            <input


            name="amount"


            type="number"


            placeholder="Payment amount"


            value={
                form.amount
            }



            onChange={change}



            className="
                border
                rounded-lg
                p-3
                w-full
                mt-6
            "


            />








            <input


            name="transaction_id"


            placeholder="Transaction ID"



            value={
                form.transaction_id
            }



            onChange={change}



            className="
                border
                rounded-lg
                p-3
                w-full
                mt-3
            "


            />









            <input


            type="file"


            accept="image/*"



            onChange={fileChange}



            className="
                border
                rounded-lg
                p-3
                w-full
                mt-3
            "


            />









            <button


            disabled={loading}



            onClick={submitPayment}



            className="
                bg-green-600
                text-white
                rounded-lg
                p-3
                w-full
                mt-5
            "


            >


                {

                    loading

                    ?

                    "Submitting..."

                    :

                    "Submit Payment Proof"


                }


            </button>





        </div>


    );


}
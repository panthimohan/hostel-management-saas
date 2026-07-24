import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";

import client from "../api/client";


const EMPTY_FORM = {
    hostel: "",
    title: "",
    payment_type: "BANK",
    account_name: "",
    account_number: "",
    qr_image: null,
};



export default function PaymentQRManager(){

    const [qrs, setQrs] = useState([]);

    const [hostels, setHostels] = useState([]);

    const [open, setOpen] = useState(false);

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState(EMPTY_FORM);

    const [error, setError] = useState("");



    async function load(){

        try{

            setError("");

            const [
                qrRes,
                hostelRes
            ] = await Promise.all([

                client.get(
                    "/payments/payment-qrs/"
                ),

                client.get(
                    "/hostels/"
                )

            ]);



            console.log(
                "HOSTELS:",
                hostelRes.data
            );



            const hostelList =
                hostelRes.data.results ??
                hostelRes.data ??
                [];



            setQrs(

                qrRes.data.results ??
                qrRes.data ??
                []

            );


            setHostels(
                hostelList
            );


        }

        catch(err){

            console.log(
                "LOAD ERROR:",
                err.response?.data
            );


            setError(

                err.response?.data?.detail
                ||
                "Unable to load hostels"

            );


            setHostels([]);

        }

    }





    useEffect(()=>{

        load();

    },[]);







    function change(e){

        setForm(prev=>({

            ...prev,

            [e.target.name]:
            e.target.value

        }));

    }







    function fileChange(e){

        setForm(prev=>({

            ...prev,

            qr_image:
            e.target.files[0]

        }));

    }








    async function saveQR(){

        setError("");



        if(!form.hostel){

            setError(
                "Please select hostel"
            );

            return;

        }



        if(!form.title){

            setError(
                "Enter QR title"
            );

            return;

        }



        if(!form.qr_image){

            setError(
                "Upload QR image"
            );

            return;

        }



        try{


            setLoading(true);



            const data = new FormData();



            data.append(
                "hostel",
                form.hostel
            );


            data.append(
                "title",
                form.title
            );


            data.append(
                "payment_type",
                form.payment_type
            );


            data.append(
                "account_name",
                form.account_name
            );


            data.append(
                "account_number",
                form.account_number
            );


            data.append(
                "qr_image",
                form.qr_image
            );





            await client.post(

                "/payments/payment-qrs/",

                data,

                {
                    headers:{
                        "Content-Type":
                        "multipart/form-data"
                    }
                }

            );



            setForm(
                EMPTY_FORM
            );


            setOpen(false);


            await load();


        }


        catch(err){


            console.log(
                err.response?.data
            );


            setError(

                JSON.stringify(
                    err.response?.data
                    ||
                    "Unable to save QR"
                )

            );


        }


        finally{

            setLoading(false);

        }

    }








    async function remove(id){


        if(
            !window.confirm(
                "Delete QR?"
            )
        )

        return;



        try{


            await client.delete(

                `/payments/payment-qrs/${id}/`

            );


            load();


        }

        catch(err){

            console.log(err);

        }


    }








    return (

    <div className="card p-5">


        <div className="
            flex
            justify-between
            items-center
            mb-5
        ">


            <div>

                <h2 className="text-lg font-semibold">
                    Payment QR Codes
                </h2>


                <p className="text-sm text-gray-500">
                    Available hostels: {hostels.length}
                </p>

            </div>




            <button

                onClick={()=>{

                    setError("");

                    setOpen(true);

                }}

                className="
                bg-blue-600
                text-white
                px-4
                py-2
                rounded-lg
                flex
                items-center
                gap-2
                "

            >

                <Plus size={18}/>

                Add QR

            </button>


        </div>







        {
            error &&

            <div className="
                bg-red-100
                text-red-700
                p-3
                rounded-lg
                mb-4
            ">

                {error}

            </div>

        }







        <div className="
            grid
            md:grid-cols-3
            gap-5
        ">


        {
            qrs.map(qr=>(


                <div

                key={qr.id}

                className="
                border
                rounded-lg
                p-4
                "

                >


                    <h3 className="font-semibold">

                        {qr.title}

                    </h3>


                    <p className="text-sm text-gray-500">

                        {qr.payment_type}

                    </p>



                    <img

                        src={qr.qr_image}

                        className="
                        w-full
                        h-48
                        object-contain
                        mt-3
                        "

                    />



                    <button

                        onClick={()=>remove(qr.id)}

                        className="
                        text-red-600
                        mt-3
                        flex
                        gap-2
                        "

                    >

                        <Trash2 size={16}/>

                        Delete

                    </button>


                </div>


            ))
        }


        </div>








        {
        open &&


        <div className="
            mt-6
            border
            rounded-lg
            p-5
            space-y-4
        ">


            <select

                name="hostel"

                value={form.hostel}

                onChange={change}

                className="
                border
                p-2
                rounded
                w-full
                "

            >

                <option value="">

                    Select Hostel

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





            <input

                name="title"

                value={form.title}

                onChange={change}

                placeholder="QR Title"

                className="
                border
                p-2
                rounded
                w-full
                "

            />





            <select

                name="payment_type"

                value={form.payment_type}

                onChange={change}

                className="
                border
                p-2
                rounded
                w-full
                "

            >

                <option value="BANK">
                    Bank
                </option>


                <option value="ESEWA">
                    eSewa
                </option>


                <option value="KHALTI">
                    Khalti
                </option>


                <option value="FONEPAY">
                    FonePay
                </option>


            </select>





            <input

                name="account_name"

                value={form.account_name}

                onChange={change}

                placeholder="Account Name"

                className="
                border
                p-2
                rounded
                w-full
                "

            />





            <input

                name="account_number"

                value={form.account_number}

                onChange={change}

                placeholder="Account Number"

                className="
                border
                p-2
                rounded
                w-full
                "

            />





            <input

                type="file"

                onChange={fileChange}

                className="
                border
                p-2
                rounded
                w-full
                "

            />





            <button

                disabled={loading}

                onClick={saveQR}

                className="
                bg-green-600
                text-white
                px-5
                py-2
                rounded-lg
                "

            >

                {
                    loading
                    ?
                    "Saving..."
                    :
                    "Save QR"
                }


            </button>



        </div>

        }


    </div>

    );

}
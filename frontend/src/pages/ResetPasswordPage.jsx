import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import client from "../api/client";


export default function ResetPasswordPage() {


  const [searchParams] = useSearchParams();

  const navigate = useNavigate();


  const uid = searchParams.get("uid");

  const token = searchParams.get("token");



  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);



  async function handleSubmit(e) {

    e.preventDefault();


    setMessage("");

    setError("");

    setLoading(true);



    try {


      const response = await client.post(

        "/auth/password-reset/confirm/",

        {

          uid,

          token,

          new_password: password

        }

      );



      setMessage(
        response.data.detail
      );



      setTimeout(()=>{

        navigate("/login");

      },2000);



    } catch(err){


      setError(

        err.response?.data?.detail ||

        "Password reset failed."

      );


    } finally {

      setLoading(false);

    }


  }




  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">


      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">


        <h1 className="text-2xl font-bold mb-6">

          Reset Password

        </h1>



        <form onSubmit={handleSubmit}>


          <input

            type="password"

            placeholder="New password"

            value={password}

            onChange={(e)=>setPassword(e.target.value)}

            className="w-full border p-3 rounded mb-4"

            required

          />


          <button

            disabled={loading}

            className="w-full bg-green-600 text-white p-3 rounded"

          >

            {loading ? "Resetting..." : "Reset Password"}

          </button>


        </form>



        {message && (

          <div className="mt-4 p-3 bg-green-100">

            {message}

          </div>

        )}



        {error && (

          <div className="mt-4 p-3 bg-red-100">

            {error}

          </div>

        )}


      </div>


    </div>

  );

}
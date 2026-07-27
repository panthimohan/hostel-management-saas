import { useState } from "react";
import client from "../api/client";
import { Link } from "react-router-dom";


export default function ForgotPasswordPage() {

  const [email, setEmail] = useState("");
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
        "/auth/password-reset/",
        {
          email
        }
      );


      setMessage(
        response.data.reset_url
          ? `Reset link generated: ${response.data.reset_url}`
          : response.data.detail
      );


    } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }

  }



  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">

        <h1 className="text-2xl font-bold mb-6">
          Forgot Password
        </h1>


        <form onSubmit={handleSubmit}>


          <label className="block mb-2">
            Email
          </label>


          <input

            type="email"

            value={email}

            onChange={(e)=>setEmail(e.target.value)}

            className="w-full border p-3 rounded mb-4"

            placeholder="Enter your email"

            required

          />


          <button

            disabled={loading}

            className="w-full bg-blue-600 text-white p-3 rounded"

          >

            {loading ? "Sending..." : "Send Reset Link"}

          </button>


        </form>



        {message && (

          <div className="mt-4 p-3 bg-green-100 break-all">

            {message}

          </div>

        )}



        {error && (

          <div className="mt-4 p-3 bg-red-100">

            {error}

          </div>

        )}



        <Link

          to="/login"

          className="block mt-5 text-blue-600"

        >

          Back to Login

        </Link>


      </div>

    </div>

  );

}
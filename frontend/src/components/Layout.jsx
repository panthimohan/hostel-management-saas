import {
  Building2,
  DoorClosed,
  LayoutGrid,
  LogOut,
  Receipt,
  ShieldCheck,
  User as UserIcon,
  Users,
  CreditCard,
} from "lucide-react";

import { NavLink } from "react-router-dom";

import { useAuth } from "../context/AuthContext";


const NAV_BY_ROLE = {

  SUPER_ADMIN: [
    {
      to: "/",
      label: "Organizations",
      icon: ShieldCheck
    },
  ],


  HOSTEL_OWNER: [

    {
      to: "/",
      label: "Dashboard",
      icon: LayoutGrid
    },

    {
      to: "/hostels",
      label: "Hostels",
      icon: Building2
    },

    {
      to: "/rooms",
      label: "Rooms & Beds",
      icon: DoorClosed
    },

    {
      to: "/tenants",
      label: "Tenants",
      icon: Users
    },

    {
      to: "/expenses",
      label: "Expenses",
      icon: Receipt
    },

    {
      to: "/payments",
      label: "Payments",
      icon: CreditCard
    },

  ],


  HOSTEL_MANAGER: [

    {
      to: "/",
      label: "Dashboard",
      icon: LayoutGrid
    },

    {
      to: "/hostels",
      label: "Hostels",
      icon: Building2
    },

    {
      to: "/rooms",
      label: "Rooms & Beds",
      icon: DoorClosed
    },

    {
      to: "/tenants",
      label: "Tenants",
      icon: Users
    },

    {
      to: "/expenses",
      label: "Expenses",
      icon: Receipt
    },

    {
      to: "/payments",
      label: "Payments",
      icon: CreditCard
    },

  ],


  TENANT: [

    {
      to: "/",
      label: "My Room",
      icon: UserIcon
    },

    {
      to: "/payments",
      label: "My Payments",
      icon: CreditCard
    },

  ],

};




export default function Layout({ children }) {


  const { user, logout } = useAuth();

  const navItems =
    NAV_BY_ROLE[user?.role] || [];



  return (

    <div className="
      min-h-screen
      flex
      flex-col
      md:flex-row
      overflow-x-hidden
      w-full
    ">


      {/* Sidebar */}

      <aside className="
        hidden
        md:flex
        md:w-64
        md:flex-col
        md:fixed
        md:inset-y-0
        border-r
        border-border
        bg-surface
      ">


        <div className="
          px-6
          py-6
          border-b
          border-border
        ">

          <span className="
            font-display
            text-2xl
            font-semibold
            text-primary
          ">
            Nestled
          </span>


          <p className="
            text-xs
            text-ink-soft
            mt-0.5
          ">
            Hostel operations, in one place
          </p>

        </div>




        <nav className="
          flex-1
          px-3
          py-4
          space-y-1
          overflow-y-auto
        ">


          {
            navItems.map(({to,label,icon:Icon})=>(

              <NavLink

                key={to}

                to={to}

                end={to === "/"}

                className={({isActive}) =>

                  `
                  flex
                  items-center
                  gap-3
                  rounded-lg
                  px-3
                  py-2.5
                  text-sm
                  font-medium
                  transition-colors
                  ${
                    isActive
                    ?
                    "bg-primary/10 text-primary-dark"
                    :
                    "text-ink-soft hover:bg-fog hover:text-ink"
                  }
                  `

                }

              >

                <Icon size={18}/>

                {label}

              </NavLink>

            ))
          }


        </nav>





        <div className="
          px-3
          py-4
          border-t
          border-border
        ">


          <div className="
            px-3
            py-2
            mb-1
          ">

            <p className="
              text-sm
              font-medium
              text-ink
              truncate
            ">
              {user?.email}
            </p>


            <p className="
              text-xs
              text-ink-soft
            ">
              {user?.role?.replace(/_/g," ")}
            </p>

          </div>




          <button

            onClick={logout}

            className="
              flex
              w-full
              items-center
              gap-3
              rounded-lg
              px-3
              py-2.5
              text-sm
              font-medium
              text-clay
              hover:bg-clay-light
            "

          >

            <LogOut size={18}/>

            Log out

          </button>


        </div>


      </aside>







      {/* Mobile Header */}

      <header className="
        md:hidden
        flex
        items-center
        justify-between
        px-4
        py-3
        border-b
        border-border
        bg-surface
      ">


        <span className="
          font-display
          text-xl
          font-semibold
          text-primary
        ">
          Nestled
        </span>



        <button
          onClick={logout}
          className="
            p-2
            rounded-lg
            text-clay
          "
        >

          <LogOut size={20}/>

        </button>


      </header>








      {/* Main Content */}

      <main className="
        flex-1
        md:ml-64
        w-full
        min-w-0
        overflow-x-hidden
        px-4
        py-6
        md:px-8
        md:py-8
        pb-24
        md:pb-8
      ">


        <div className="
          w-full
          min-w-0
        ">

          {children}

        </div>


      </main>








      {/* Mobile Bottom Navigation */}

      <nav className="
        md:hidden
        fixed
        bottom-0
        inset-x-0
        z-30
        bg-surface
        border-t
        border-border
        flex
        justify-around
        py-2
      ">


        {
          navItems.map(({to,label,icon:Icon})=>(


            <NavLink

              key={to}

              to={to}

              end={to === "/"}

              className={({isActive})=>

                `
                flex
                flex-col
                items-center
                gap-1
                px-3
                py-1.5
                rounded-lg
                text-[11px]
                font-medium
                ${
                  isActive
                  ?
                  "text-primary-dark"
                  :
                  "text-ink-soft"
                }
                `

              }

            >

              <Icon size={20}/>

              {label}

            </NavLink>


          ))
        }


      </nav>


    </div>

  );

}
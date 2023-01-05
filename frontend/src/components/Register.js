import React, { useState } from "react";
import "./Login.css";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import {
	MDBBtn,
	MDBContainer,
	MDBRow,
	MDBCol,
	MDBCard,
	MDBCardBody,
	MDBInput,
	MDBIcon,
} from "mdb-react-ui-kit";

export default function Register() {
	const [first_name, setFirstname] = useState(null);
	const [last_name, setLastname] = useState(null);
	const [email, setEmail] = useState(null);
	const [username, setUsername] = useState(null);
	const [password, setPassword] = useState(null);
	const [phone, setPhone] = useState(null);
	const [address, setAddress] = useState(null);

	var userData = {
		username,
		password,
		email,
		first_name,
		last_name,
		phone,
		address,
	};
	function createUser() {
		fetch("http://localhost:8000/users/create", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(userData),
		})
			.then((response) => response.json())
			.then((data) => console.log(data));
	}

	return (
		<MDBContainer fluid>
			<MDBRow className="d-flex justify-content-center align-items-center h-100">
				<MDBCol col="12">
					<MDBCard
						className="bg-dark text-white my-5 mx-auto"
						style={{ borderRadius: "1rem", maxWidth: "400px" }}
					>
						<MDBCardBody className="p-5 d-flex flex-column align-items-center mx-auto w-100">
							<h2 className="fw-bold mb-2 text-uppercase">
								Register
							</h2>
							<p className="text-white-50 mb-5">
								Welcome to our site!
							</p>
							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="First Name"
								type="text"
								size="lg"
								onChange={(e) => setFirstname(e.target.value)}
							/>

							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Last Name"
								type="text"
								size="lg"
								onChange={(e) => setLastname(e.target.value)}
							/>
							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Email address"
								type="email"
								size="lg"
								onChange={(e) => setEmail(e.target.value)}
							/>
							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Username"
								type="text"
								size="lg"
								onChange={(e) => setUsername(e.target.value)}
							/>

							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Password"
								type="password"
								size="lg"
								onChange={(e) => setPassword(e.target.value)}
							/>

							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Phone Number"
								type="number"
								size="lg"
								onChange={(e) => setPhone(e.target.value)}
							/>

							<MDBInput
								className="text-white"
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Address"
								type="text"
								size="lg"
								onChange={(e) => setAddress(e.target.value)}
							/>
							<MDBBtn
								className="mx-5 mt-2 px-5"
								size="lg"
								onClick={createUser}
							>
								Register
							</MDBBtn>
						</MDBCardBody>
					</MDBCard>
				</MDBCol>
			</MDBRow>
		</MDBContainer>
	);
}

//return (
//	<button
//		onClick={createUser}
//		style={{
//			textAlign: "center",
//			width: "100px",
//			border: "1px solid gray",
//			borderRadius: "5px",
//		}}
//	>
//		Send data to backend
//	</button>
//);

import react, { useState } from "react";
import { useNavigate } from "react-router-dom";
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

export default function Login() {
	const navigate = useNavigate();

	const [username, setUsername] = useState(null);
	const [password, setPassword] = useState(null);

	const fetchToken = (username, password) => {
		const options = {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({
				grant_type: "password",
				username: username,
				password: password,
			}),
		};

		fetch("http://localhost:8000/token", options)
			.then((response) => response.json())
			.then((response) =>
				localStorage.setItem("token", response.access_token)
			)
			.catch((err) => console.error(err));
	};

	const signUp = () => {
		navigate("/register");
	};

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
								Login
							</h2>
							<p className="text-white-50 mb-5">
								Please enter your login and password!
							</p>

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

							<p className="small mb-3 pb-lg-2">
								<a class="text-white-50" href="#!">
									Forgot password?
								</a>
							</p>
							<MDBBtn className="mx-2 px-5" size="lg">
								Login
							</MDBBtn>
							<div>
								<p className="mt-5 mb-0">
									Don't have an account?{" "}
									<a
										href="/register"
										class="text-white-50 fw-bold"
										onClick={fetchToken(username, password)}
									>
										Sign Up
									</a>
								</p>
							</div>
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

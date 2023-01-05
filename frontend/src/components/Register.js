import react from "react";
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
	var userData = {
		role: "regular",
		username: "bob",
		password: "bob",
		email: "bob",
		first_name: "bob",
		last_name: "bob",
		phone: "1873246",
		address: "Su ema",
		create_permission: false,
		read_permission: false,
		update_permission: false,
		delete_permission: false,
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
								Login
							</h2>
							<p className="text-white-50 mb-5">
								Please enter your login and password!
							</p>

							<MDBInput
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Email address"
								id="formControlLg"
								type="email"
								size="lg"
							/>
							<MDBInput
								wrapperClass="mb-4 mx-5 w-100"
								labelClass="text-white"
								label="Password"
								id="formControlLg"
								type="password"
								size="lg"
							/>

							<p className="small mb-3 pb-lg-2">
								<a class="text-white-50" href="#!">
									Forgot password?
								</a>
							</p>
							<MDBBtn
								outline
								className="mx-2 px-5"
								color="white"
								size="lg"
							>
								Login
							</MDBBtn>

							<div className="d-flex flex-row mt-3 mb-5">
								<MDBBtn
									tag="a"
									color="none"
									className="m-3"
									style={{ color: "white" }}
								>
									<MDBIcon fab icon="google" size="lg" />
								</MDBBtn>
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
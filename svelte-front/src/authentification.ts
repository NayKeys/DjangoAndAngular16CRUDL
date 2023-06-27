
export const casLoginUrl = "https://cas.ensea.fr/login";
export function loginWithCAS() {
	// replace this URL with the actual login endpoint
	window.location.href = casLoginUrl;
}

export async function validateCASTicket(ticket) {
	const response = await fetch("/api/validate_cas_ticket", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			ticket: ticket,
		}),
	});
	const data = await response.json();
	if (data.token) {
		localStorage.setItem("jwt", data.token);
	}
}

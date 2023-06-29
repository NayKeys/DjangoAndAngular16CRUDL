import { getMeta } from "./main";

export const casLoginUrl = "https://cas.ensea.fr/login";
export function loginWithCAS() {
	// replace this URL with the actual login endpoint
	window.location.href = casLoginUrl;
}

export async function validateCASTicket(csrfToken: string, ticket: string): Promise<string | undefined> {
	const response = await fetch("/api/cas/", {
		method: "POST",
		headers: {
			"X-CSRFToken": csrfToken,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			ticket: ticket,
		}),
	});
	const res = await response.json();
	if (res.status != 200) {
		return undefined;
	}
	if (res.jwt) {
		localStorage.setItem("jwt", res.jwt); // Useless???
	}
	return res.jwt;
}

export async function validateJWTToken(csrfToken: string, token: string): Promise<boolean> {
	const response = await fetch("/api/auth/", {
		method: "PUT",
		headers: {
			"X-CSRFToken": csrfToken,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			jwt: token,
		}),
	});
	const res = await response.json();
	if (res.status == 200) {
		return true;
	}
	return false;
}

export async function logout() {  // Copilot generated
  const response = await fetch("/api/auth/", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("jwt"),
    }),
  });
  const res = await response.json();
  if (res.status == 200) {
    localStorage.removeItem("jwt");
  }
}
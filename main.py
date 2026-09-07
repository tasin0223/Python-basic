from datetime import datetime
import requests


def audit_website(domain):
    # ইউআরএল ফরম্যাট ঠিক করা
    if not domain.startswith("http://") and not domain.startswith("https://"):
        target_url = "https://" + domain
    else:
        target_url = domain

    print(f"\n[+] Analyzing: {target_url}")
    print("=" * 50)

    try:
        # রেসপন্স ফেচ করা (টাইমআউট ৫ সেকেন্ড)
        response = requests.get(target_url, timeout=5)
        headers = response.headers

        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Server Header: {headers.get('Server', 'Hidden / Unknown')}\n")

        # গুরুত্বপূর্ণ সিকিউরিটি হেডারসমূহের তালিকা
        security_headers = {
            "Content-Security-Policy": "Prevents XSS attacks",
            "Strict-Transport-Security": "Enforces HTTPS connections",
            "X-Frame-Options": "Protects against Clickjacking",
            "X-Content-Type-Options": "Prevents MIME-sniffing",
        }

        report_data = []
        report_data.append(f"SECURITY AUDIT REPORT: {target_url}")
        report_data.append(
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_data.append("=" * 50)

        print("--- Security Headers Status ---")
        for header, description in security_headers.items():
            if header in headers:
                status = f"[PRESENT] {header}"
                print(f"\033[92m{status}\033[0m")  # সবুজ রঙে প্রিন্ট
                report_data.append(f"{status} -> {headers[header]}")
            else:
                status = f"[MISSING] {header} ({description})"
                print(f"\033[91m{status}\033[0m")  # লাল রঙে প্রিন্ট
                report_data.append(status)

        # ফাইল হ্যান্ডেলিং: রিপোর্ট সেভ করা
        file_name = "audit_report.txt"
        with open(file_name, "w") as file:
            file.write("\n".join(report_data))

        print("=" * 50)
        print(f"[✓] Report saved to '{file_name}'")

    except requests.exceptions.RequestException as e:
        print(f"[!] Connection failed: {e}")


if __name__ == "__main__":
    print("----------------------------------------")
    print("      Basic Web Security Auditor        ")
    print("----------------------------------------")
    target = input("Enter target website (e.g. example.com): ").strip()
    if target:
        audit_website(target)
    else:
        print("[!] No website entered.")



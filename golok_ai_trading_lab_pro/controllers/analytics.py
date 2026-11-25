from datetime import datetime, timezone
from urllib.parse import urlsplit

from odoo import http
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request


class AnalyticsCredential(http.Controller):
    @http.route("/golok/analytics/credential", type="http", auth="user", methods=["GET", "POST"], csrf=True)
    def credential(self, company_id=None, credential=None, expiry=None, **_ignored):
        response = {"code": "REQUEST_REJECTED"}
        status = 400
        try:
            env = request.env
            request_id = int(company_id)
            if request_id not in env.user.company_ids.ids:
                raise AccessError("Invalid company")
            service = env["golok.lab.analytics.config"].with_context(allowed_company_ids=[request_id])
            service._admin()
            if request.httprequest.method == "GET":
                response = {"csrf": request.csrf_token(), **service._public_status(service._current())}
            else:
                browser = request.httprequest
                if not browser.is_secure and (browser.remote_addr not in ("127.0.0.1", "::1")
                                              or urlsplit(browser.host_url).hostname not in ("localhost", "127.0.0.1", "::1")):
                    raise AccessError("Secure transport required")
                if request.httprequest.content_length is None or request.httprequest.content_length > 12_000:
                    raise ValueError
                if not isinstance(expiry, str) or len(expiry) > 32:
                    raise ValueError
                stamp = datetime.fromisoformat(expiry)
                if stamp.utcoffset() is None:
                    raise ValueError
                response = service._store(credential, stamp.astimezone(timezone.utc).replace(tzinfo=None))
            status = 200
        except AccessError:
            response, status = {"code": "ACCESS_DENIED"}, 403
        except (TypeError, ValueError, ValidationError):
            pass
        return request.make_json_response(response, status=status, headers=[("Cache-Control", "no-store")])

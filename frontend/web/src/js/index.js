/* @format */
/* jshint esversion: 10, globalstrict: true */
"use strict";

let detectedPublicIp = "";

window.onload = () => {
    if (window.location.pathname === "/controlloDDNS") {
        window.location.replace("/controlloDDNS/");
        return;
    }

    initializeState();
    setupEventListeners();
    const routeAction = applyCheckRoute();

    loadPublicIp();

    if (routeAction === "ports") {
        handleSubmit(new Event("submit"));
    }

    if (routeAction === "ddns") {
        handleDdnsSubmit(new Event("submit"));
    }
};

const reservedPaths = new Set([
    "api",
    "css",
    "docs",
    "favicon.ico",
    "js",
    "metrics",
    "privacy-policy",
    "robots.txt",
    "sitemap.xml",
    "come-verificare-se-una-porta-e-aperta",
    "test-port-forwarding",
    "porte-tcp-comuni",
    "porte-pericolose-da-aprire",
    "ip-pubblico-nat-cgnat",
    "perche-una-porta-risulta-chiusa",
    "usare-controlloporte-con-chatgpt-claude",
]);

// Reactive state
const state = new Proxy(
    {
        host: "",
        ports: [],
        results: null,
        ddnsResults: null,
        loading: false,
        ddnsLoading: false,
        error: null,
    },
    {
        set(target, prop, value) {
            target[prop] = value;
            updateView(prop, value);
            return true;
        },
    }
);

function initializeState() {
    state.host = "";
    state.ports = [];
    state.results = null;
    state.ddnsResults = null;
    state.loading = false;
    state.ddnsLoading = false;
    state.error = null;
}

function setupEventListeners() {
    const form = document.getElementById("form");
    const portsInput = document.getElementById("ports");

    // Form submission
    form.addEventListener("submit", handleSubmit);

    // Quick port buttons
    document.querySelectorAll(".quick-port-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            if (btn.dataset.ports) {
                setPorts(btn.dataset.ports);
            } else {
                addPort(btn.dataset.port);
            }
            btn.classList.add("active");
            setTimeout(() => btn.classList.remove("active"), 200);
        });
    });

    document.getElementById("copy-share-link")?.addEventListener("click", copyShareLink);
    document.getElementById("copy-ddns-share-link")?.addEventListener("click", copyDdnsShareLink);
    document.getElementById("ddns-submit")?.addEventListener("click", handleDdnsSubmit);
    document.getElementById("use-public-ip")?.addEventListener("click", usePublicIp);

    // Validate ports on input
    portsInput.addEventListener("input", () => {
        validatePortsInput();
    });

    // Validate host on input
    document.getElementById("host").addEventListener("input", () => {
        validateHostInput();
    });
}

function handleSubmit(event) {
    event.preventDefault();
    event.stopPropagation();

    const hostValid = validateHostInput();
    const portsValid = validatePortsInput();

    if (!hostValid || !portsValid) {
        return;
    }

    hideError();
    hideResults();
    hideDdnsResults();
    queryHost();
}

function handleDdnsSubmit(event) {
    event.preventDefault();
    event.stopPropagation();

    if (!validateDdnsHostInput()) {
        return;
    }

    hideError();
    hideResults();
    hideDdnsResults();
    queryDdns();
}

function validateHostInput() {
    const hostInput = document.getElementById("host");
    const hostGroup = hostInput.closest(".form-group");
    const value = hostInput.value.trim();

    // Allow hostname, IPv4, or "me"
    const hostPattern = /^([\w-]+(\.[\w-]+)*|me|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/;
    const isValid = value && hostPattern.test(value);

    hostGroup.classList.toggle("has-error", !isValid);
    return isValid;
}

function validatePortsInput() {
    const portsInput = document.getElementById("ports");
    const portsGroup = portsInput.closest(".form-group");
    const value = portsInput.value.trim();

    if (!value) {
        portsGroup.classList.add("has-error");
        return false;
    }

    const ports = value
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean);
    const isValid = ports.every((p) => {
        const num = parseInt(p, 10);
        return !isNaN(num) && num >= 1 && num <= 65535;
    });

    portsGroup.classList.toggle("has-error", !isValid || ports.length === 0);
    return isValid && ports.length > 0;
}

function addPort(port) {
    const portsInput = document.getElementById("ports");
    const currentPorts = portsInput.value
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean);

    if (!currentPorts.includes(port)) {
        currentPorts.push(port);
        portsInput.value = currentPorts.join(", ");
    }

    validatePortsInput();
}

function setPorts(ports) {
    document.getElementById("ports").value = ports
        .split(",")
        .map((port) => port.trim())
        .filter(Boolean)
        .join(", ");

    validatePortsInput();
}

function applyCheckRoute() {
    const segments = window.location.pathname
        .split("/")
        .filter(Boolean)
        .map((segment) => decodeURIComponent(segment));

    if (isDdnsRoute(segments)) {
        return applyDdnsRoute(segments);
    }

    if (![1, 2].includes(segments.length) || reservedPaths.has(segments[0])) {
        return false;
    }

    const [host, ports = ""] = segments;
    document.getElementById("host").value = host;

    if (!ports) {
        validateHostInput();
        return false;
    }

    document.getElementById("ports").value = ports.replaceAll(";", ", ");

    return validateHostInput() && validatePortsInput() ? "ports" : false;
}

function isDdnsRoute(segments) {
    return segments[0] === "controlloDDNS";
}

function applyDdnsRoute(segments) {
    if (segments.length > 2) {
        return false;
    }

    const host = segments[1] || "";
    if (host) {
        document.getElementById("host").value = host;
    }

    document.body.classList.add("ddns-route");

    if (!host) {
        return false;
    }

    return validateDdnsHostInput() ? "ddns" : false;
}

function loadPublicIp() {
    fetch("/api/me")
        .then((response) => response.text())
        .then((response) => {
            const publicIp = response.trim();
            const publicIpValue = document.getElementById("public-ip-value");
            const usePublicIpButton = document.getElementById("use-public-ip");

            detectedPublicIp = publicIp;

            if (publicIpValue) {
                publicIpValue.textContent = publicIp;
            }

            if (usePublicIpButton) {
                usePublicIpButton.disabled = false;
            }
        })
        .catch((e) => {
            const publicIpValue = document.getElementById("public-ip-value");

            if (publicIpValue) {
                publicIpValue.textContent = "non rilevabile";
            }

            console.log("Failed to detect IP:", e);
        });
}

function usePublicIp() {
    if (!detectedPublicIp) {
        return;
    }

    state.host = detectedPublicIp;
    document.getElementById("host").value = detectedPublicIp;
    validateHostInput();
}

function queryHost() {
    const form = document.getElementById("form");
    const host = form.querySelector("#host").value.trim();
    const ports = form
        .querySelector("#ports")
        .value.split(",")
        .map((p) => p.trim())
        .filter(Boolean);

    state.host = host;
    state.loading = true;
    state.error = null;

    fetch("/api/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ host: host, ports: ports }),
    })
        .then((response) =>
            response.json().then((data) => {
                if (!response.ok) {
                    const error = new Error(data?.message || "Request failed");
                    error.data = data;
                    throw error;
                }

                return data;
            })
        )
        .then((response) => {
            state.results = response;
            state.loading = false;
        })
        .catch((error) => {
            state.error =
                error.data?.extra?.map((item) => item.message).join(", ") ||
                error.data?.message ||
                "Si è verificato un errore. Riprova tra poco.";
            state.loading = false;
        });
}

function queryDdns() {
    const form = document.getElementById("form");
    const host = form.querySelector("#host").value.trim();

    state.host = host;
    state.ddnsLoading = true;
    state.error = null;

    fetch("/api/controlloDDNS", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ host: host }),
    })
        .then((response) =>
            response.json().then((data) => {
                if (!response.ok) {
                    const error = new Error(data?.message || "Request failed");
                    error.data = data;
                    throw error;
                }

                return data;
            })
        )
        .then((response) => {
            state.ddnsResults = response;
            state.ddnsLoading = false;
        })
        .catch((error) => {
            state.error =
                error.data?.extra?.map((item) => item.message).join(", ") ||
                error.data?.message ||
                "Si è verificato un errore. Riprova tra poco.";
            state.ddnsLoading = false;
        });
}

function validateDdnsHostInput() {
    const hostInput = document.getElementById("host");
    const hostGroup = hostInput.closest(".form-group");
    const value = hostInput.value.trim();
    const hostnamePattern = /^[\w-]+(\.[\w-]+)+$/;
    const isValid = value && hostnamePattern.test(value);

    hostGroup.classList.toggle("has-error", !isValid);
    return isValid;
}

function updateView(prop, value) {
    const submitBtn = document.getElementById("submit");
    const ddnsSubmitBtn = document.getElementById("ddns-submit");

    switch (prop) {
        case "loading":
            submitBtn.classList.toggle("loading", value);
            submitBtn.disabled = value;
            break;

        case "ddnsLoading":
            if (ddnsSubmitBtn) {
                ddnsSubmitBtn.classList.toggle("loading", value);
                ddnsSubmitBtn.disabled = value;
            }
            break;

        case "results":
            if (value && !state.error) {
                showResults(value);
            }
            break;

        case "ddnsResults":
            if (value && !state.error) {
                showDdnsResults(value);
            }
            break;

        case "error":
            if (value) {
                showError(value);
            }
            break;
    }
}

function showResults(data) {
    const resultsDiv = document.getElementById("results");
    const resultsHost = document.getElementById("results-host");
    const resultsList = document.getElementById("results-list");
    const shareUrlInput = document.getElementById("share-url");
    const introContent = document.getElementById("intro-content");

    resultsHost.textContent = data.host;
    resultsList.innerHTML = "";

    data.check.forEach((check) => {
        const item = document.createElement("div");
        item.className = "result-item";

        const isOpen = check.status === true || check.status === "True";
        const statusClass = isOpen ? "open" : "closed";
        const statusText = isOpen ? "Aperta" : "Chiusa";
        const hasLatency =
            isOpen &&
            check.latency_ms !== null &&
            check.latency_ms !== undefined &&
            Number.isFinite(Number(check.latency_ms));
        const latencyText = hasLatency ? `${check.latency_ms} ms` : "";

        item.innerHTML = `
            <span class="result-port">Porta ${check.port}</span>
            <span class="result-latency">${latencyText}</span>
            <span class="result-status ${statusClass}">
                <span class="status-dot"></span>
                ${statusText}
            </span>
        `;

        resultsList.appendChild(item);
    });

    resultsDiv.classList.remove("hidden");
    if (shareUrlInput) {
        shareUrlInput.value = buildShareUrl(data);
    }
    introContent?.classList.add("hidden");
    scrollToFeedback(resultsDiv);
}

function showDdnsResults(data) {
    const resultsDiv = document.getElementById("ddns-results");
    const resultsHost = document.getElementById("ddns-results-host");
    const resultCard = document.getElementById("ddns-result-card");
    const shareUrlInput = document.getElementById("ddns-share-url");
    const introContent = document.getElementById("intro-content");
    const statusClass = data.match ? "open" : "closed";
    const statusText = data.match ? "DDNS corretto" : "DDNS non allineato";

    resultsHost.textContent = data.host;
    resultCard.innerHTML = `
        <div class="ddns-status ${statusClass}">
            <span class="status-dot"></span>
            ${statusText}
        </div>
        <dl class="ddns-details">
            <div>
                <dt>IP del visitatore</dt>
                <dd>${data.requester_ip}</dd>
            </div>
            <div>
                <dt>IP risolto dal nome host</dt>
                <dd>${data.resolved_ip}</dd>
            </div>
        </dl>
    `;

    resultsDiv.classList.remove("hidden");
    if (shareUrlInput) {
        shareUrlInput.value = buildDdnsShareUrl(data);
    }
    introContent?.classList.add("hidden");
    scrollToFeedback(resultsDiv);
}

function hideResults() {
    document.getElementById("results").classList.add("hidden");
    document.getElementById("intro-content")?.classList.remove("hidden");
}

function hideDdnsResults() {
    document.getElementById("ddns-results").classList.add("hidden");
    document.getElementById("intro-content")?.classList.remove("hidden");
}

function showError(message) {
    const errorDiv = document.getElementById("error");
    const errorText = document.getElementById("error-text");

    errorText.textContent = message;
    errorDiv.classList.remove("hidden");
    scrollToFeedback(errorDiv);
}

function hideError() {
    document.getElementById("error").classList.add("hidden");
}

function scrollToFeedback(element) {
    element?.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
}

function buildShareUrl(data) {
    const host = encodeURIComponent(data.host);
    const ports = data.check.map((check) => check.port).join(",");

    return `${window.location.origin}/${host}/${ports}`;
}

function buildDdnsShareUrl(data) {
    const host = encodeURIComponent(data.host);

    return `${window.location.origin}/controlloDDNS/${host}`;
}

function copyShareLink() {
    const shareUrlInput = document.getElementById("share-url");
    const copyButton = document.getElementById("copy-share-link");

    copyToClipboard(shareUrlInput, copyButton);
}

function copyDdnsShareLink() {
    const shareUrlInput = document.getElementById("ddns-share-url");
    const copyButton = document.getElementById("copy-ddns-share-link");

    copyToClipboard(shareUrlInput, copyButton);
}

function copyToClipboard(shareUrlInput, copyButton) {
    if (!shareUrlInput || !copyButton) {
        return;
    }

    const originalText = copyButton.textContent;
    const value = shareUrlInput.value;
    const setCopied = () => {
        copyButton.textContent = "Copiato";
        setTimeout(() => {
            copyButton.textContent = originalText;
        }, 1600);
    };

    if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(value).then(setCopied).catch(() => {
            shareUrlInput.select();
        });
        return;
    }

    shareUrlInput.select();
    document.execCommand("copy");
    setCopied();
}

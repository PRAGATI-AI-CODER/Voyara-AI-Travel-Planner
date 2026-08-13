"use client";

import { useState } from "react";

const travelStyles = ["Adventure", "Relaxed", "Luxury", "Budget"];

const interests = [
  "Food",
  "Nature",
  "Culture",
  "History",
  "Nightlife",
  "Shopping",
];

interface TripFormData {
  destination: string;
  start_date: string;
  end_date: string;
  travelers: number;
  budget: number;
  travel_style: string[];
  interests: string[];
}

export default function TripForm() {
  const [formData, setFormData] = useState<TripFormData>({
    destination: "",
    start_date: "",
    end_date: "",
    travelers: 2,
    budget: 0,
    travel_style: [],
    interests: [],
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const toggleItem = (
    item: string,
    field: "travel_style" | "interests",
  ) => {
    setFormData((current) => ({
      ...current,
      [field]: current[field].includes(item)
        ? current[field].filter((value) => value !== item)
        : [...current[field], item],
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/trips", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        const validationMessage =
          data.detail?.[0]?.msg || "Something went wrong.";

        throw new Error(validationMessage);
      }

      setMessage("Trip received successfully! Voyara is ready to plan.");
      console.log("Voyara API response:", data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the Voyara API.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      id="trip-planner"
      className="min-h-screen bg-white px-6 py-24"
    >
      <div className="mx-auto max-w-4xl">
        <div className="mb-12 text-center">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
            Build your journey
          </p>

          <h2 className="text-4xl font-semibold tracking-tight text-gray-900 sm:text-5xl">
            Tell us what makes your
            <span className="block text-gray-500">perfect trip.</span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-gray-600">
            Give Voyara a few details. We&apos;ll use them to understand your
            travel preferences and build a personalized journey.
          </p>
        </div>

        <div className="rounded-3xl border border-black/10 bg-[#f8f9f6] p-6 shadow-sm sm:p-10">
          <div className="grid gap-8">
            <div>
              <label
                htmlFor="destination"
                className="mb-3 block text-sm font-semibold text-gray-900"
              >
                Where do you want to go?
              </label>

              <input
                id="destination"
                type="text"
                value={formData.destination}
                onChange={(event) =>
                  setFormData({
                    ...formData,
                    destination: event.target.value,
                  })
                }
                placeholder="e.g. Kyoto, Japan"
                className="w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
              />
            </div>

            <div className="grid gap-6 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="start-date"
                  className="mb-3 block text-sm font-semibold text-gray-900"
                >
                  Start date
                </label>

                <input
                  id="start-date"
                  type="date"
                  value={formData.start_date}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      start_date: event.target.value,
                    })
                  }
                  className="w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-gray-700 outline-none transition focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                />
              </div>

              <div>
                <label
                  htmlFor="end-date"
                  className="mb-3 block text-sm font-semibold text-gray-900"
                >
                  End date
                </label>

                <input
                  id="end-date"
                  type="date"
                  value={formData.end_date}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      end_date: event.target.value,
                    })
                  }
                  className="w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-gray-700 outline-none transition focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                />
              </div>
            </div>

            <div className="grid gap-6 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="travelers"
                  className="mb-3 block text-sm font-semibold text-gray-900"
                >
                  Number of travelers
                </label>

                <input
                  id="travelers"
                  type="number"
                  min="1"
                  max="50"
                  value={formData.travelers}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      travelers: Number(event.target.value),
                    })
                  }
                  className="w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-gray-900 outline-none transition focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                />
              </div>

              <div>
                <label
                  htmlFor="budget"
                  className="mb-3 block text-sm font-semibold text-gray-900"
                >
                  Approximate budget
                </label>

                <input
                  id="budget"
                  type="number"
                  min="1"
                  value={formData.budget || ""}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      budget: Number(event.target.value),
                    })
                  }
                  placeholder="50000"
                  className="w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                />
              </div>
            </div>

            <div>
              <p className="mb-4 text-sm font-semibold text-gray-900">
                What&apos;s your travel style?
              </p>

              <div className="flex flex-wrap gap-3">
                {travelStyles.map((style) => {
                  const selected = formData.travel_style.includes(style);

                  return (
                    <button
                      key={style}
                      type="button"
                      onClick={() => toggleItem(style, "travel_style")}
                      className={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                        selected
                          ? "border-gray-900 bg-gray-900 text-white"
                          : "border-gray-200 bg-white text-gray-700 hover:border-gray-400"
                      }`}
                    >
                      {style}
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <p className="mb-4 text-sm font-semibold text-gray-900">
                What are you interested in?
              </p>

              <div className="flex flex-wrap gap-3">
                {interests.map((interest) => {
                  const selected = formData.interests.includes(interest);

                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => toggleItem(interest, "interests")}
                      className={`rounded-full border px-5 py-2.5 text-sm font-medium transition ${
                        selected
                          ? "border-gray-900 bg-gray-900 text-white"
                          : "border-gray-200 bg-white text-gray-700 hover:border-gray-400"
                      }`}
                    >
                      {interest}
                    </button>
                  );
                })}
              </div>
            </div>

            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="mt-2 w-full rounded-2xl bg-gray-900 px-6 py-4 text-base font-semibold text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Building your journey..." : "Build My Journey →"}
            </button>

            {message && (
              <div className="rounded-2xl border border-green-200 bg-green-50 px-5 py-4 text-sm font-medium text-green-800">
                {message}
              </div>
            )}

            {error && (
              <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm font-medium text-red-800">
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
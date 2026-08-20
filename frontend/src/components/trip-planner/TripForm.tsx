"use client";

import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

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

interface ItineraryDay {
  day: number;
  date: string;
  destination: string;
  morning: string;
  afternoon: string;
  evening: string;
}

interface ItineraryResponse {
  message: string;
  trip_id: number;
  destination: string;
  start_date: string;
  end_date: string;
  metadata: {
    duration_days: number;
    travelers: number;
    budget: number;
    travel_style: string;
    interests: string[];
    planning_type: string;
  };
  itinerary: ItineraryDay[];
}

const formatDate = (date: string) => {
  if (!date) return "";

  return new Date(`${date}T00:00:00`).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const formatBudget = (budget: number) => {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
  }).format(budget);
};

const getPlanningLabel = (planningType: string) => {
  if (planningType === "ai") {
    return "AI planned";
  }

  if (planningType === "deterministic-fallback") {
    return "Fallback plan";
  }

  return "Smart plan";
};

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
  const [itinerary, setItinerary] =
    useState<ItineraryResponse | null>(null);

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
    setItinerary(null);

    try {
      const createResponse = await fetch(
        `${API_BASE_URL}/api/trips`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        },
      );

      const tripData = await createResponse.json();

      if (!createResponse.ok) {
        const validationMessage =
          tripData.detail?.[0]?.msg ||
          tripData.detail ||
          "Unable to create trip.";

        throw new Error(validationMessage);
      }

      const tripId = tripData.trip?.id;

      if (!tripId) {
        throw new Error(
          "Trip was created, but no trip ID was returned.",
        );
      }

      setMessage(
        "Trip created. Voyara is planning your journey...",
      );

      const itineraryResponse = await fetch(
        `${API_BASE_URL}/api/trips/${tripId}/plan`,
      );

      const itineraryData =
        await itineraryResponse.json();

      if (!itineraryResponse.ok) {
        const planningMessage =
          itineraryData.detail?.[0]?.msg ||
          itineraryData.detail ||
          "Unable to generate itinerary.";

        throw new Error(planningMessage);
      }

      setItinerary(itineraryData);

      setMessage(
        itineraryData.metadata?.planning_type === "ai"
          ? "Your AI-powered journey is ready."
          : "Your journey is ready.",
      );

      console.log(
        "Voyara itinerary:",
        itineraryData,
      );
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
      <div className="mx-auto max-w-5xl">
        <div className="mb-12 text-center">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
            Build your journey
          </p>

          <h2 className="text-4xl font-semibold tracking-tight text-gray-900 sm:text-5xl">
            Tell us what makes your
            <span className="block text-gray-500">
              perfect trip.
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-gray-600">
            Give Voyara a few details. We&apos;ll use them to
            understand your travel preferences and build a
            personalized journey.
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
                  const selected =
                    formData.travel_style.includes(style);

                  return (
                    <button
                      key={style}
                      type="button"
                      onClick={() =>
                        toggleItem(style, "travel_style")
                      }
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
                  const selected =
                    formData.interests.includes(interest);

                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() =>
                        toggleItem(interest, "interests")
                      }
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
              {loading
                ? "Voyara is planning..."
                : "Build My Journey →"}
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

            {itinerary && (
              <div className="mt-12 space-y-8">
                {/* Journey header */}
                <div className="rounded-3xl bg-gray-900 p-7 text-white shadow-sm sm:p-9">
                  <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                      <div className="mb-3 flex items-center gap-2">
                        <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-gray-200">
                          {getPlanningLabel(
                            itinerary.metadata.planning_type,
                          )}
                        </span>

                        <span className="text-xs text-gray-400">
                          Trip #{itinerary.trip_id}
                        </span>
                      </div>

                      <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-400">
                        Your Voyara Journey
                      </p>

                      <h3 className="mt-2 text-4xl font-semibold tracking-tight sm:text-5xl">
                        {itinerary.destination}
                      </h3>

                      <p className="mt-3 text-gray-300">
                        {formatDate(itinerary.start_date)}{" "}
                        <span className="mx-2 text-gray-500">
                          →
                        </span>{" "}
                        {formatDate(itinerary.end_date)}
                      </p>
                    </div>

                    <div className="grid grid-cols-2 gap-3 sm:min-w-[260px]">
                      <JourneyStat
                        label="Duration"
                        value={`${itinerary.metadata.duration_days} days`}
                      />

                      <JourneyStat
                        label="Travelers"
                        value={`${itinerary.metadata.travelers}`}
                      />

                      <JourneyStat
                        label="Budget"
                        value={`₹${formatBudget(
                          itinerary.metadata.budget,
                        )}`}
                      />

                      <JourneyStat
                        label="Style"
                        value={itinerary.metadata.travel_style}
                      />
                    </div>
                  </div>

                  {itinerary.metadata.interests.length > 0 && (
                    <div className="mt-7 border-t border-white/10 pt-5">
                      <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
                        Your interests
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {itinerary.metadata.interests.map(
                          (interest) => (
                            <span
                              key={interest}
                              className="rounded-full bg-white/10 px-3 py-1.5 text-xs font-medium text-gray-200"
                            >
                              {interest}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* Daily itinerary */}
                <div className="space-y-5">
                  {itinerary.itinerary.map((day) => (
                    <div
                      key={day.day}
                      className="overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-sm transition duration-300 hover:-translate-y-0.5 hover:shadow-md"
                    >
                      <div className="border-b border-gray-100 bg-[#f8f9f6] px-6 py-5 sm:px-7">
                        <div className="flex items-center gap-4">
                          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-gray-900 text-sm font-bold text-white">
                            {day.day}
                          </div>

                          <div>
                            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
                              Day {day.day}
                            </p>

                            <h4 className="mt-1 text-xl font-semibold text-gray-900">
                              {formatDate(day.date)}
                            </h4>
                          </div>
                        </div>
                      </div>

                      <div className="grid gap-0 md:grid-cols-3">
                        <ActivityBlock
                          title="Morning"
                          icon="☀"
                          content={day.morning}
                          border
                        />

                        <ActivityBlock
                          title="Afternoon"
                          icon="◌"
                          content={day.afternoon}
                          border
                        />

                        <ActivityBlock
                          title="Evening"
                          icon="☾"
                          content={day.evening}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="rounded-2xl border border-gray-200 bg-gray-50 px-5 py-4 text-center text-sm text-gray-500">
                  Your itinerary is personalized around your selected
                  destination, budget, travel style, and interests.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

function JourneyStat({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-white/10 px-4 py-3">
      <p className="text-xs text-gray-400">{label}</p>
      <p className="mt-1 truncate text-sm font-semibold text-white">
        {value}
      </p>
    </div>
  );
}

function ActivityBlock({
  title,
  icon,
  content,
  border = false,
}: {
  title: string;
  icon: string;
  content: string;
  border?: boolean;
}) {
  return (
    <div
      className={`p-6 sm:p-7 ${
        border
          ? "border-b border-gray-100 md:border-b-0 md:border-r"
          : ""
      }`}
    >
      <div className="mb-3 flex items-center gap-2">
        <span className="text-sm text-gray-400">{icon}</span>

        <p className="text-sm font-semibold text-gray-900">
          {title}
        </p>
      </div>

      <p className="text-sm leading-7 text-gray-600">
        {content}
      </p>
    </div>
  );
}
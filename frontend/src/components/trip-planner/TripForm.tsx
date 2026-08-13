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

export default function TripForm() {
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);

  const toggleItem = (
    item: string,
    selected: string[],
    setSelected: React.Dispatch<React.SetStateAction<string[]>>,
  ) => {
    setSelected((current) =>
      current.includes(item)
        ? current.filter((value) => value !== item)
        : [...current, item],
    );
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
                  defaultValue="2"
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
                  min="0"
                  placeholder="₹50,000"
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
                  const selected = selectedStyles.includes(style);

                  return (
                    <button
                      key={style}
                      type="button"
                      onClick={() =>
                        toggleItem(
                          style,
                          selectedStyles,
                          setSelectedStyles,
                        )
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
                  const selected = selectedInterests.includes(interest);

                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() =>
                        toggleItem(
                          interest,
                          selectedInterests,
                          setSelectedInterests,
                        )
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
              className="mt-2 w-full rounded-2xl bg-gray-900 px-6 py-4 text-base font-semibold text-white transition hover:bg-gray-700"
            >
              Build My Journey →
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
// src/components/dashboard/ManagerDashboard.tsx

import useSWR from "swr";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import toast from "react-hot-toast";
import { useAuth } from "@/hooks/useAuth";
import { Input } from "../ui/input";
import { useState } from "react";
import { Label } from "../ui/label";
import { Archive } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Spinner } from "../ui/spinner";

interface Feedback {
  id: string;
  sentiment: string;
  created_at: string;
}

interface TeamFeedback {
  employee_id: string;
  employee_name: string;
  feedback_count: number;
  feedbacks: Feedback[];
}

export default function ManagerDashboard() {
  const { fetcher } = useAuth();
  const navigate = useNavigate();
  const { data, error, isLoading } = useSWR("/dashboard", fetcher);

  const [search, setSearch] = useState("");

  if (error) {
    toast.error("Failed to load dashboard");
    return <div className="text-red-500">Error loading dashboard.</div>;
  }

  if (isLoading || !data) return <div className="flex justify-center items-center h-screen"><Spinner show={true} size="large" /></div>;

  const { sentiment_summary, team_feedback } = data;

  const filteredFeedbacks = team_feedback.filter((fb: TeamFeedback) =>
    fb.employee_name.toLowerCase().includes(search.toLowerCase())
  );

  if (filteredFeedbacks.length === 0) {
    return (
      <div className="text-center text-sm text-muted-foreground flex flex-col items-center justify-center gap-2 h-screen">
        <Archive className="w-10 h-10" />
        <p>No employee found</p>
        <p className="text-xs text-muted-foreground">
          Try searching for a different employee
        </p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6 w-full">
      {/* Sentiment Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Sentiment Summary</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-4">
          {["positive", "neutral", "negative"].map((key) => (
            <div key={key} className="text-center">
              <div className="text-sm text-muted-foreground capitalize">
                {key}
              </div>
              <div className="text-2xl font-bold">
                {sentiment_summary[key as keyof typeof sentiment_summary] || 0}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      <Label>
        <p className="text-sm text-nowrap">Search employee: </p>
        <Input
          type="text"
          placeholder="Search employee"
          className="w-full text-sm placeholder:text-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Label>

      {/* Team Feedback */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredFeedbacks.map((member: TeamFeedback) => (
          <Card
            key={member.employee_id}
            onClick={() => navigate(`/employee/${member.employee_id}`)}
            className="hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          >
            <CardHeader>
              <CardTitle>{member.employee_name}</CardTitle>
              <div className="text-sm text-muted-foreground">
                {member.feedback_count} feedback
                {member.feedback_count !== 1 && "s"}
              </div>
            </CardHeader>
            <CardContent className="space-y-2">
              {member.feedbacks.map((fb: Feedback, index: number) => (
                <div
                  key={fb.id}
                  className="flex justify-between items-center text-sm"
                >
                  <div
                    className={`text-xs px-3 py-1 rounded-md ${
                      fb.sentiment === "positive"
                        ? "bg-green-100 text-green-800 border border-green-300"
                        : fb.sentiment === "neutral"
                        ? "bg-yellow-100 text-yellow-800 border border-yellow-300"
                        : fb.sentiment === "negative"
                        ? "bg-red-100 text-red-800 border border-red-300"
                        : ""
                    }`}
                  >
                    {fb.sentiment?.charAt(0).toUpperCase() +
                      fb.sentiment?.slice(1)}
                  </div>
                  <span className="text-muted-foreground">
                    {new Date(fb.created_at).toLocaleString()}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

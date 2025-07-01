import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import useSWR from "swr";
import { SparklesIcon, MessageCircleIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import toast from "react-hot-toast";
import { useAuth } from "@/hooks/useAuth";


export default function EmployeeDashboard() {
  const { fetcher, apiClient } = useAuth();

  // Get feedbacks
  const { data, error, isLoading } = useSWR("/feedbacks/me", fetcher);

  // Get assigned manager
  const { data: teamData } = useSWR("/feedback-requests/my-manager", fetcher);
  const managerId = teamData?.id;

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!managerId) {
      toast.error("No manager assigned.");
      return;
    }

    setLoading(true);
    try {   
    const res = await apiClient.post("/feedback-requests", { manager_id: managerId, message });

    if (res.status === 200) {
      toast.success("Feedback request sent!");
      setMessage("");
    } else {
        toast.error("Failed to send request");
      }
    } catch (error) {
      toast.error("Failed to send request");
    } finally {
      setLoading(false);
    }
  };

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading feedbacks</p>;

  return (
    <div className="p-6 max-w-[800px] space-y-10 w-full">
      {/* Request Feedback */}
      <form onSubmit={handleRequest} className="space-y-4">
        <h2 className="text-xl font-semibold">Request Feedback</h2>
        <div className="space-y-2">
          <label className="block font-medium">Message (optional)</label>
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="e.g., I’d appreciate feedback on my recent project."
          />
        </div>
        <Button type="submit" disabled={loading || !managerId || message.length < 5}>
          {loading ? "Requesting..." : "Request Feedback"}
        </Button>
      </form>

      {/* Feedback History */}
      <div className="space-y-6 w-full">
        <h2 className="text-xl font-semibold">Your Feedback History</h2>
        {data.length === 0 ? (
          <p>No feedbacks yet.</p>
        ) : (
          data.map((fb: any) => (
            <Card key={fb.id} className="border rounded-xl shadow-sm">
              <CardHeader className="flex flex-row justify-between items-start">
                <CardTitle className="text-md">From Manager</CardTitle>
                <Badge variant="outline">{fb.sentiment}</Badge>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div className="flex flex-col gap-2">
                  <div className="flex gap-2 font-medium">
                    <SparklesIcon className="h-4 w-4 mt-1 text-green-600" />
                    <p>Strengths</p>
                  </div>
                  <p>{fb.strengths}</p>
                </div>
                <div className="flex flex-col gap-2">
                  <div className="flex gap-2 font-medium">
                    <MessageCircleIcon className="h-4 w-4 mt-1 text-yellow-600" />
                    <p>Areas to Improve</p>
                  </div>
                  <p>{fb.areas_to_improve}</p>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}

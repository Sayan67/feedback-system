import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeftIcon, MessageCircleIcon, SparklesIcon } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { useParams } from "react-router-dom";
import useSWR from "swr";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function EmployeeDetailPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { fetcher } = useAuth();
  const { data, error, isLoading } = useSWR(
    `/feedbacks/employee/${id}`,
    fetcher
  );

  if (isLoading) return <Skeleton className="h-20 w-full" />;
  if (error) return <div>Error loading feedbacks.</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div>
        <Button variant="outline" className="mb-4" onClick={() => navigate("/dashboard")}>
            <ArrowLeftIcon className="w-4 h-4" />
            Back
        </Button>
        <h1 className="text-3xl font-bold mb-6">Feedback Summary</h1>
      </div>
      <div className="space-y-6">
        {data?.map((fb: any) => (
          <Card
            key={fb.id}
            className="shadow-md border border-muted rounded-2xl hover:border-primary transition"
          >
            <CardHeader className="flex flex-row justify-between items-start">
              <div className="space-y-1">
                <CardTitle className="text-lg font-semibold">
                  Feedback
                </CardTitle>
                <span className="text-sm text-muted-foreground">
                  {new Date(fb.created_at).toLocaleString()}
                </span>
              </div>
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
                {fb.sentiment?.charAt(0).toUpperCase() + fb.sentiment?.slice(1)}
              </div>
            </CardHeader>

            <CardContent className="space-y-4 text-sm">
              <div className="flex gap-2 items-start">
                <SparklesIcon className="h-4 w-4 mt-1 text-green-600" />
                <div>
                  <p className="font-medium text-muted-foreground mb-1">
                    Strengths
                  </p>
                  <p>{fb.strengths}</p>
                </div>
              </div>

              <div className="flex gap-2 items-start">
                <MessageCircleIcon className="h-4 w-4 mt-1 text-yellow-600" />
                <div>
                  <p className="font-medium text-muted-foreground mb-1">
                    Areas to Improve
                  </p>
                  <p>{fb.areas_to_improve}</p>
                </div>
              </div>

              {fb.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-2">
                  {fb.tags.map((tag: any) => (
                    <Badge
                      key={tag.id}
                      variant="outline"
                      className="bg-muted px-2"
                    >
                      {tag.name}
                    </Badge>
                  ))}
                </div>
              )}
              {fb.reply && (
                <div className="pt-4 border-t border-muted">
                  <p className="font-medium text-muted-foreground mb-1">
                    Employee Response
                  </p>
                  <p className="italic text-sm text-foreground">{fb.reply}</p>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

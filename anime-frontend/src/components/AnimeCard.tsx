interface AnimeCardProps {
    title: string;
    imageUrl: string;
    score: number;
  }
  
  export default function AnimeCard({ title, imageUrl, score }: AnimeCardProps) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4">
        <img src={imageUrl} alt={title} className="w-full h-60 object-cover rounded-md" />
        <h2 className="text-lg font-bold mt-2">{title}</h2>
        <p className="text-gray-600">Score: {score}</p>
      </div>
    );
  }
  
using System.Collections.Generic;
using System.Threading.Tasks;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
{
    public interface IVideoPathRepository
    {
        Task<VideoPath> Get(int id);
        Task<IEnumerable<string>> GetAll();
        Task Add(VideoPath videoPath);
        Task Delete(string videoName);
        Task Update(VideoPath videoPath);
    }
}
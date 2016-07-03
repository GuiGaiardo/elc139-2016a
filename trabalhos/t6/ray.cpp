#include <list>
#include <iostream>
#include <limits>
#include <cmath>
#include <mpi.h>
#include <stdlib.h>
#include <cstdio>
#include <sys/time.h>


long wall_time()
{
    struct timeval t;
    gettimeofday(&t, NULL);
    return t.tv_sec*1000000 + t.tv_usec;
}


using namespace std;

numeric_limits<double> real;
double delta = sqrt(real.epsilon()), infinity = real.infinity();

struct Vec {
  double x, y, z;
  Vec(double x2, double y2, double z2) : x(x2), y(y2), z(z2) {}
};
Vec operator+(const Vec &a, const Vec &b)
{ return Vec(a.x+b.x, a.y+b.y, a.z+b.z); }
Vec operator-(const Vec &a, const Vec &b)
{ return Vec(a.x-b.x, a.y-b.y, a.z-b.z); }
Vec operator*(double a, const Vec &b) { return Vec(a*b.x, a*b.y, a*b.z); }
double dot(const Vec &a, const Vec &b) { return a.x*b.x + a.y*b.y + a.z*b.z; }
Vec unitise(const Vec &a) { return (1 / sqrt(dot(a, a))) * a; }

typedef pair<double, Vec> Hit;

struct Ray {
  Vec orig, dir;
  Ray(const Vec &o, const Vec &d) : orig(o), dir(d) {}
};

struct Scene {
  virtual ~Scene() {};
  virtual Hit intersect(const Hit &, const Ray &) const = 0;
};

struct Sphere : public Scene {
  Vec center;
  double radius;

  Sphere(Vec c, double r) : center(c), radius(r) {}
  ~Sphere() {}

  double ray_sphere(const Ray &ray) const {
    Vec v = center - ray.orig;
    double b = dot(v, ray.dir), disc = b*b - dot(v, v) + radius * radius;
    if (disc < 0) return infinity;
    double d = sqrt(disc), t2 = b + d;
    if (t2 < 0) return infinity;
    double t1 = b - d;
    return (t1 > 0 ? t1 : t2);
  }

  Hit intersect(const Hit &hit, const Ray &ray) const {
    double lambda = ray_sphere(ray);
    if (lambda >= hit.first) return hit;
    return Hit(lambda, unitise(ray.orig + lambda*ray.dir - center));
  }
};

typedef list<Scene *> Scenes;
struct Group : public Scene {
  Sphere bound;
  Scenes child;

  Group(Sphere b, Scenes c) : bound(b), child(c) {}
  ~Group() {
    for (Scenes::const_iterator it=child.begin(); it!=child.end(); ++it)
      delete *it;
  }

  Hit intersect(const Hit &hit, const Ray &ray) const {
    Hit hit2=hit;
    double l = bound.ray_sphere(ray);
    if (l >= hit.first) return hit;
    for (Scenes::const_iterator it=child.begin(); it!=child.end(); ++it)
      hit2 = (*it)->intersect(hit2, ray);
    return hit2;
  }
};

Hit intersect(const Ray &ray, const Scene &s)
{ return s.intersect(Hit(infinity, Vec(0, 0, 0)), ray); }

double ray_trace(const Vec &light, const Ray &ray, const Scene &s) {
  Hit hit = intersect(ray, s);
  if (hit.first == infinity) return 0;
  double g = dot(hit.second, light);
  if (g >= 0) return 0.;
  Vec p = ray.orig + hit.first*ray.dir + delta*hit.second;
  return (intersect(Ray(p, -1. * light), s).first < infinity ? 0 : -g);
}

Scene *create(int level, const Vec &c, double r) {
  Scene *s = new Sphere(c, r);
  if (level == 1) return s;
  Scenes child;
  child.push_back(s);
  double rn = 3*r/sqrt(12.);
  for (int dz=-1; dz<=1; dz+=2)
    for (int dx=-1; dx<=1; dx+=2)
      child.push_back(create(level-1, c + rn*Vec(dx, 1, dz), r/2));
  return new Group(Sphere(c, 3*r), child);
}

void recieve_and_print(int n_workers, int n, int chunk){
  long tempo_inicial, tempo_final;
  char cabecalho[12];
  FILE *f = fopen("img1.ppm", "w");

  int job_counter[n_workers], msg[n], img[n][n], msg_counter = 0, source, row, i;
  MPI_Status status;

  for (i=0; i<n_workers; i++){
    job_counter[i] = 0;
  }

  tempo_inicial = wall_time();

  while (msg_counter < n){
    MPI_Recv(msg, n, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    msg_counter++;

    source = n_workers - status.MPI_SOURCE;

    row = source * chunk + job_counter[source];
    for (i=0; i<n; i++){
      img[row][i] = msg[i];
    }
    job_counter[source]++;
  }

  tempo_final = wall_time();

  printf("\nTempo calculos = %ld usec", (long) (tempo_final - tempo_inicial));

  sprintf(cabecalho, "P5\n%d %d\n255\n", n, n);
  fputs(cabecalho, f);
  //cout << "P5\n" << n << " " << n << "\n255\n";

  tempo_inicial = wall_time();

  for (i=0; i<n; i++){
    for (int j=0; j<n; j++){
      fputc(img[i][j], f);
      //cout << char(img[i][j]);
    }
  }

  tempo_final = wall_time();
  printf("\nTempo escrita = %ld usec", (long) (tempo_final - tempo_inicial));

  return;
}


int main(int argc, char *argv[]) {
  int level = 6, n = 512, ss = 4, i;
  if (argc == 2) level = atoi(argv[1]);

  //MPI initialization   ########################
  int my_rank, n_process, dest, chunk, n_workers;
  dest = 0;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
  MPI_Comm_size(MPI_COMM_WORLD, &n_process);
  n_workers = n_process-1;
  chunk = n/n_workers;
  //#############################################

  if (my_rank == 0){
    recieve_and_print(n_workers, n, chunk);
  }

  else{
    //Work load division######################
    int my_init, my_end;

    if (my_rank == n_workers){
      my_init = (n_workers-1)*chunk;
      my_end = n;
    }
    else{
      my_init = (my_rank-1)*chunk;
      my_end = my_init + chunk;
    }
    //########################################
    int count, msg[n];

    Vec light = unitise(Vec(-1, -3, 2));
    Scene *s(create(level, Vec(0, -1, 0), 1));
    for (int y=my_end-1; y>=my_init; --y){
      count = 0;
      for (int x=0; x<n; ++x) {
        double g=0;
        for (int dx=0; dx<ss; ++dx)
          for (int dy=0; dy<ss; ++dy) {
            Vec dir(unitise(Vec(x+dx*1./ss-n/2., y+dy*1./ss-n/2., n)));
            g += ray_trace(light, Ray(Vec(0, 0, -4), dir), *s);
          }
        msg[count] = int(.5 + 255. * g / (ss*ss));
        count++;
      }
      MPI_Send(msg, n, MPI_INT, dest, 0, MPI_COMM_WORLD);
    }
    delete s;
  }

  MPI_Finalize();
  return 0;
}
